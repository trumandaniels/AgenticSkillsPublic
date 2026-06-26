#!/usr/bin/env python3
"""Initialize ProPlay-inspired procedural memory files for a Codex skill."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

PROCEDURAL_SECTION = """## Procedural Memory

For tasks that resemble prior episodes, read `references/procedure-memory.md`, inspect `references/procedure-graph.json`, and run `scripts/retrieve_memory.py` with the current task summary before drafting the task plan. Retrieval requires local embeddings and combines RRF, dense similarity, and task-specific transition reliability when available.

Use the retrieval pack to preplay a likely path: review similar failures, select relevant procedure nodes, note reliable transitions, and identify failure patterns to avoid. Prefer transitions with supporting task-specific reliability when present. Treat the preplay as soft guidance; user instructions and fresh task evidence override stale memory.

Default to automatic capture. Before the final response, record a compact episode with `scripts/record_episode.py` when the run contains reusable procedural signal. Include planned trace, executed trace, outcome/reward, productive prefix, failure suffix, procedure candidates, and local validation signal when available.

After recording, run `scripts/refine_graph.py` to update procedure nodes, observed transitions, reward-weighted transition reliability, and failure patterns from the episode. Use local `sentence-transformers` embeddings; do not call paid APIs from refinement scripts.

Do not skip capture unless the user explicitly confirms skipping for this run. If capture seems low-signal, sensitive, or evaluation-contaminating, ask the user to confirm skip; otherwise record a minimal sanitized episode.

End with a procedural-memory receipt: `recorded <episode_id>` or `skipped by explicit user confirmation because <reason>`.
"""

RETRIEVE_MEMORY_SCRIPT = r'''#!/usr/bin/env python3
"""Retrieve procedural memory with required dense embeddings plus RRF."""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9_\-]+", (text or "").lower())


def stable_id(item: dict, prefix: str, index: int) -> str:
    for key in ("id", "failure_id", "pattern_id", "episode_id", "edge_id", "node_id"):
        if item.get(key):
            return str(item[key])
    return f"{prefix}_{index}"


def stringify(value) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return " ".join(stringify(v) for v in value)
    if isinstance(value, dict):
        return " ".join(stringify(v) for v in value.values())
    return str(value)


def item_text(item: dict) -> str:
    fields = [
        "task_family", "request_summary", "task_text", "summary", "label", "pattern",
        "context", "avoidance", "avoid_rule", "corrective_tactic", "lessons",
        "failure_patterns", "procedures_used", "procedure_trace", "condition", "from", "to",
    ]
    return " | ".join(stringify(item.get(field)) for field in fields if item.get(field))


def collect_failure_candidates(graph: dict) -> list[dict]:
    candidates = []
    for index, pattern in enumerate(graph.get("failure_patterns", [])):
        item = dict(pattern)
        item["kind"] = "failure_pattern"
        item["candidate_id"] = stable_id(item, "failure_pattern", index)
        item["retrieval_text"] = item_text(item)
        candidates.append(item)
    for index, episode in enumerate(graph.get("episodes", [])):
        outcome = str(episode.get("outcome", episode.get("status", ""))).lower()
        has_failure = bool(episode.get("failure_patterns"))
        if has_failure or any(word in outcome for word in ("fail", "partial", "reject", "skipped")):
            item = dict(episode)
            item["kind"] = "episode_failure"
            item["candidate_id"] = stable_id(item, "episode", index)
            item["retrieval_text"] = item_text(item)
            candidates.append(item)
    return candidates


def collect_transition_candidates(graph: dict) -> list[dict]:
    candidates = []
    for index, edge in enumerate(graph.get("edges", [])):
        item = dict(edge)
        item["kind"] = "transition"
        item["candidate_id"] = stable_id(item, "edge", index)
        item["retrieval_text"] = item_text(item)
        candidates.append(item)
    return candidates


def bm25_rank(candidates: list[dict], query: str) -> list[str]:
    query_terms = tokenize(query)
    if not query_terms or not candidates:
        return []
    docs = [tokenize(c.get("retrieval_text") or item_text(c)) for c in candidates]
    avgdl = sum(len(doc) for doc in docs) / max(len(docs), 1)
    df = Counter(term for doc in docs for term in set(doc))
    scores = {}
    k1 = 1.5
    b = 0.75
    for candidate, doc in zip(candidates, docs):
        tf = Counter(doc)
        score = 0.0
        for term in query_terms:
            if tf[term] == 0:
                continue
            idf = math.log(1 + (len(docs) - df[term] + 0.5) / (df[term] + 0.5))
            denom = tf[term] + k1 * (1 - b + b * len(doc) / max(avgdl, 1e-9))
            score += idf * (tf[term] * (k1 + 1)) / denom
        if score > 0:
            scores[candidate["candidate_id"]] = score
    return [cid for cid, _ in sorted(scores.items(), key=lambda pair: pair[1], reverse=True)]


def procedure_overlap_rank(candidates: list[dict], procedures: Iterable[str], query: str) -> list[str]:
    proc_terms = set(tokenize(" ".join(procedures))) | {t for t in tokenize(query) if t.startswith("proc_")}
    if not proc_terms:
        return []
    scores = {}
    for candidate in candidates:
        text_terms = set(tokenize(stringify(candidate.get("procedures_used")) + " " + stringify(candidate.get("procedure_trace")) + " " + stringify(candidate.get("from")) + " " + stringify(candidate.get("to"))))
        overlap = len(proc_terms & text_terms)
        if overlap:
            scores[candidate["candidate_id"]] = overlap
    return [cid for cid, _ in sorted(scores.items(), key=lambda pair: pair[1], reverse=True)]


def failure_pattern_rank(candidates: list[dict], query: str) -> list[str]:
    q = set(tokenize(query))
    scores = {}
    for candidate in candidates:
        pattern_text = stringify(candidate.get("failure_patterns")) + " " + stringify(candidate.get("pattern")) + " " + stringify(candidate.get("label")) + " " + stringify(candidate.get("candidate_id"))
        overlap = len(q & set(tokenize(pattern_text)))
        if overlap:
            scores[candidate["candidate_id"]] = overlap
    return [cid for cid, _ in sorted(scores.items(), key=lambda pair: pair[1], reverse=True)]


def rrf(rankings: list[list[str]], k: int = 60) -> dict[str, float]:
    scores: dict[str, float] = defaultdict(float)
    for ranking in rankings:
        for rank, candidate_id in enumerate(ranking, start=1):
            scores[candidate_id] += 1.0 / (k + rank)
    return dict(scores)


def normalize(scores: dict[str, float], ids: Iterable[str]) -> dict[str, float]:
    ids = list(ids)
    if not ids:
        return {}
    values = [scores.get(i, 0.0) for i in ids]
    lo = min(values)
    hi = max(values)
    if hi <= lo:
        return {i: (1.0 if scores.get(i, 0.0) > 0 else 0.0) for i in ids}
    return {i: (scores.get(i, 0.0) - lo) / (hi - lo) for i in ids}


def load_embedding_model(model_name: str):
    try:
        from sentence_transformers import SentenceTransformer
    except Exception as exc:
        raise SystemExit(
            "Required embedding dependency missing. Install sentence-transformers and make "
            f"the model available locally: {model_name}. Original error: {exc}"
        ) from exc
    try:
        return SentenceTransformer(model_name, local_files_only=True)
    except Exception as exc:
        raise SystemExit(
            "Required embedding model could not be loaded. Ensure the model is installed or "
            f"cached locally in this environment: {model_name}. Original error: {exc}"
        ) from exc


def dot(a, b) -> float:
    return float(sum(float(x) * float(y) for x, y in zip(a, b)))


def norm(vec) -> float:
    return math.sqrt(max(dot(vec, vec), 0.0))


def cosine(a, b) -> float:
    denom = norm(a) * norm(b)
    if denom <= 1e-12:
        return 0.0
    return dot(a, b) / denom


def dense_scores(candidates: list[dict], query: str, model_name: str) -> dict[str, float]:
    if not candidates:
        return {}
    model = load_embedding_model(model_name)
    texts = [c.get("retrieval_text") or item_text(c) for c in candidates]
    try:
        vectors = model.encode([query] + texts, normalize_embeddings=True)
    except TypeError:
        vectors = model.encode([query] + texts)
    query_vec = vectors[0]
    return {candidate["candidate_id"]: dot(query_vec, vec) for candidate, vec in zip(candidates, vectors[1:])}


def reliability_scores(candidates: list[dict], query: str, model_name: str) -> dict[str, float]:
    model = load_embedding_model(model_name)
    try:
        query_vec = model.encode([query], normalize_embeddings=True)[0]
    except TypeError:
        query_vec = model.encode([query])[0]
    scores = {}
    for candidate in candidates:
        weight = float(candidate.get("reliability_weight_sum") or 0.0)
        vector_sum = candidate.get("reliability_vector_sum") or []
        if weight > 0 and vector_sum:
            centroid = [float(v) / weight for v in vector_sum]
            scores[candidate["candidate_id"]] = cosine(query_vec, centroid) * max(float(candidate.get("mean_reward") or 0.0), 0.0)
    return scores


def rank_candidates(candidates: list[dict], query: str, procedures: Iterable[str], rrf_k: int, model_name: str, rrf_weight: float, dense_weight: float, reliability_weight: float = 0.0) -> list[dict]:
    if not candidates:
        return []
    by_id = {candidate["candidate_id"]: candidate for candidate in candidates}
    rankings = [
        bm25_rank(candidates, query),
        procedure_overlap_rank(candidates, procedures, query),
        failure_pattern_rank(candidates, query),
    ]
    rrf_scores = rrf(rankings, k=rrf_k)
    dense = dense_scores(candidates, query, model_name)
    reliability = reliability_scores(candidates, query, model_name) if reliability_weight > 0 else {}
    ids = list(by_id)
    rrf_norm = normalize(rrf_scores, ids)
    dense_norm = normalize(dense, ids)
    reliability_norm = normalize(reliability, ids)
    has_reliability = any(reliability.get(candidate_id, 0.0) > 0 for candidate_id in ids)
    ranked = []
    for candidate_id in ids:
        item = dict(by_id[candidate_id])
        item["rrf_score"] = round(rrf_scores.get(candidate_id, 0.0), 6)
        item["rrf_norm"] = round(rrf_norm.get(candidate_id, 0.0), 6)
        item["dense_score"] = round(dense.get(candidate_id, 0.0), 6)
        item["dense_norm"] = round(dense_norm.get(candidate_id, 0.0), 6)
        item["reliability_score"] = round(reliability.get(candidate_id, 0.0), 6)
        item["reliability_norm"] = round(reliability_norm.get(candidate_id, 0.0), 6)
        hybrid_score = rrf_weight * rrf_norm.get(candidate_id, 0.0) + dense_weight * dense_norm.get(candidate_id, 0.0)
        item["final_score"] = round((1 - reliability_weight) * hybrid_score + reliability_weight * reliability_norm.get(candidate_id, 0.0) if has_reliability else hybrid_score, 6)
        ranked.append(item)
    return sorted(ranked, key=lambda item: item["final_score"], reverse=True)


def render_markdown(failures: list[dict], transitions: list[dict], inject_k: int, model_name: str) -> str:
    lines = ["## Retrieved Procedural Memory", "", f"Fusion: 75% normalized RRF + 25% dense embeddings, plus local transition reliability when available (`{model_name}`)", "", "### Similar Failures"]
    if not failures:
        lines.append("- None retrieved.")
    for item in failures[:inject_k]:
        label = item.get("label") or item.get("pattern") or item.get("request_summary") or item.get("candidate_id")
        avoid = item.get("avoidance") or item.get("avoid_rule") or item.get("corrective_tactic") or stringify(item.get("lessons")) or "No avoidance rule recorded."
        lines.append(f"- `{item['candidate_id']}` final={item['final_score']} rrf={item['rrf_norm']} dense={item['dense_norm']}: {label}")
        lines.append(f"  Avoid: {avoid}")
    lines.extend(["", "### Relevant Transitions"])
    if not transitions:
        lines.append("- None retrieved.")
    for item in transitions[:inject_k]:
        source = item.get("from") or item.get("source_id") or "?"
        target = item.get("to") or item.get("target_id") or "?"
        condition = item.get("condition") or item.get("reliability") or "No condition recorded."
        lines.append(f"- `{item['candidate_id']}` final={item['final_score']} rrf={item['rrf_norm']} dense={item['dense_norm']} rel={item.get('reliability_norm', 0)}: {source} -> {target}")
        lines.append(f"  Signal: {condition}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("graph", help="Path to references/procedure-graph.json")
    parser.add_argument("--query", required=True, help="Current task summary or retrieval query")
    parser.add_argument("--procedure", action="append", default=[], help="Active/inferred procedure id; repeat for multiple")
    parser.add_argument("--top-k", type=int, default=8, help="Candidates to keep internally")
    parser.add_argument("--inject-k", type=int, default=3, help="Compressed results to inject into preplay")
    parser.add_argument("--rrf-k", type=int, default=60, help="RRF smoothing constant")
    parser.add_argument("--embedding-model", default="sentence-transformers/all-MiniLM-L6-v2", help="Required SentenceTransformers embedding model")
    parser.add_argument("--rrf-weight", type=float, default=0.75, help="Weight for normalized RRF score")
    parser.add_argument("--dense-weight", type=float, default=0.25, help="Weight for normalized dense score")
    parser.add_argument("--reliability-weight", type=float, default=0.15, help="Weight for local task-specific transition reliability when available")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown")
    args = parser.parse_args()

    graph = json.loads(Path(args.graph).read_text(encoding="utf-8-sig"))
    failures = rank_candidates(collect_failure_candidates(graph), args.query, args.procedure, args.rrf_k, args.embedding_model, args.rrf_weight, args.dense_weight, 0.0)[: args.top_k]
    transitions = rank_candidates(collect_transition_candidates(graph), args.query, args.procedure, args.rrf_k, args.embedding_model, args.rrf_weight, args.dense_weight, args.reliability_weight)[: args.top_k]
    result = {
        "query": args.query,
        "fusion": "hybrid_rrf_dense_reliability",
        "rrf_weight": args.rrf_weight,
        "dense_weight": args.dense_weight,
        "reliability_weight": args.reliability_weight,
        "embedding_model": args.embedding_model,
        "retrieved_failures": failures[: args.inject_k],
        "ranked_transitions": transitions[: args.inject_k],
    }
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(render_markdown(failures, transitions, args.inject_k, args.embedding_model), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''

RECORD_EPISODE_SCRIPT = r'''#!/usr/bin/env python3
"""Append compact trace-aware procedural-memory episodes to procedure-graph.json."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

REQUIRED = {"task_family", "request_summary", "outcome", "procedures_used", "lessons"}


def slugify(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return value[:32] or "episode"


def parse_json_or_list(value: str | None):
    if not value:
        return []
    value = value.strip()
    if not value:
        return []
    if value[0] in "[{":
        return json.loads(value)
    return [part.strip() for part in value.split(",") if part.strip()]


def reward_from_outcome(outcome: str) -> float:
    text = (outcome or "").lower()
    if any(word in text for word in ("success", "completed", "pass", "accepted")):
        return 1.0
    if any(word in text for word in ("partial", "mixed")):
        return 0.5
    if any(word in text for word in ("fail", "reject", "error")):
        return 0.0
    return 0.25


def build_episode_from_flags(args: argparse.Namespace) -> dict:
    if not (args.task_family and args.request_summary and args.outcome):
        raise SystemExit("Provide --episode-json, --episode-file, or flags: --task-family --request-summary --outcome plus optional --procedure/--lesson/--executed-trace")
    planned_trace = parse_json_or_list(args.planned_trace)
    executed_trace = parse_json_or_list(args.executed_trace)
    procedures = args.procedure or [str(item.get("id") if isinstance(item, dict) else item) for item in (executed_trace or planned_trace)]
    return {
        "id": args.id,
        "task_family": args.task_family,
        "request_summary": args.request_summary,
        "outcome": args.outcome,
        "reward": args.reward if args.reward is not None else reward_from_outcome(args.outcome),
        "procedures_used": procedures,
        "planned_trace": planned_trace,
        "executed_trace": executed_trace,
        "productive_prefix": parse_json_or_list(args.productive_prefix),
        "failure_suffix": parse_json_or_list(args.failure_suffix),
        "procedure_candidates": parse_json_or_list(args.procedure_candidate),
        "lessons": args.lesson or [],
        "failure_patterns": args.failure_pattern or [],
        "validation_signal": args.validation_signal,
        "environment_observations": parse_json_or_list(args.environment_observations),
        "sensitivity": args.sensitivity,
        "evidence_ref": args.evidence_ref,
    }


def load_episode(args: argparse.Namespace) -> dict:
    if args.episode_json:
        episode = json.loads(args.episode_json)
    elif args.episode_file:
        episode = json.loads(Path(args.episode_file).read_text(encoding="utf-8-sig"))
    else:
        episode = build_episode_from_flags(args)
    missing = sorted(REQUIRED - set(episode))
    if missing:
        raise SystemExit(f"Episode missing required keys: {', '.join(missing)}")
    if "id" not in episode or not episode["id"]:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        episode["id"] = f"episode_{stamp}_{slugify(str(episode['task_family']))}"
    episode.setdefault("reward", reward_from_outcome(str(episode.get("outcome", ""))))
    episode.setdefault("planned_trace", [])
    episode.setdefault("executed_trace", [])
    episode.setdefault("productive_prefix", [])
    episode.setdefault("failure_suffix", [])
    episode.setdefault("procedure_candidates", [])
    episode.setdefault("failure_patterns", [])
    episode.setdefault("validation_signal", None)
    episode.setdefault("environment_observations", [])
    episode.setdefault("sensitivity", "none")
    episode.setdefault("evidence_ref", "current-thread")
    return episode


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("graph", help="Path to references/procedure-graph.json")
    parser.add_argument("--episode-json", help="Compact episode JSON object")
    parser.add_argument("--episode-file", help="Path to a JSON file containing one episode object")
    parser.add_argument("--id", help="Optional explicit episode id")
    parser.add_argument("--task-family", help="Task family for flag-based episode creation")
    parser.add_argument("--request-summary", help="Compact task summary for flag-based episode creation")
    parser.add_argument("--outcome", help="success|partial|failure|completed|skipped")
    parser.add_argument("--reward", type=float, help="Observed reward or validation score, usually 0.0 to 1.0")
    parser.add_argument("--procedure", action="append", help="Procedure id used; repeat for multiple")
    parser.add_argument("--planned-trace", help="Comma-separated ids or JSON list from preplay")
    parser.add_argument("--executed-trace", help="Comma-separated ids or JSON list representing what actually happened")
    parser.add_argument("--productive-prefix", help="Comma-separated ids or JSON list for the useful executed prefix")
    parser.add_argument("--failure-suffix", help="Comma-separated ids or JSON list for failed/corrected suffix")
    parser.add_argument("--procedure-candidate", action="append", help="JSON object/string for a reusable procedure candidate; repeat for multiple")
    parser.add_argument("--lesson", action="append", help="Reusable lesson; repeat for multiple")
    parser.add_argument("--failure-pattern", action="append", help="Failure pattern id or summary; repeat for multiple")
    parser.add_argument("--validation-signal", help="Compact test, validator, user-correction, or benchmark signal")
    parser.add_argument("--environment-observations", help="JSON or comma-separated compact observations/actions/rewards from a local adapter")
    parser.add_argument("--sensitivity", default="none", help="none|summarized|skipped_sensitive")
    parser.add_argument("--evidence-ref", default="current-thread", help="Safe pointer to source evidence")
    args = parser.parse_args()

    graph_path = Path(args.graph)
    graph = json.loads(graph_path.read_text(encoding="utf-8-sig"))
    episode = load_episode(args)
    episodes = graph.setdefault("episodes", [])
    if any(existing.get("id") == episode["id"] for existing in episodes):
        raise SystemExit(f"Episode id already exists: {episode['id']}")
    episodes.append(episode)
    graph_path.write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")
    print(f"recorded={episode['id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


REFINE_GRAPH_SCRIPT = r'''#!/usr/bin/env python3
"""Refine a procedure graph from trace-aware episodes using local embeddings."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def slug(value: str, prefix: str = "proc") -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "_", str(value).lower()).strip("_") or "unnamed"
    value = re.sub(r"_+", "_", value)
    return value if value.startswith(prefix + "_") else f"{prefix}_{value}"[:80]


def stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return " ".join(stringify(v) for v in value)
    if isinstance(value, dict):
        return " ".join(stringify(v) for v in value.values())
    return str(value)


def load_model(name: str):
    try:
        from sentence_transformers import SentenceTransformer
    except Exception as exc:
        raise SystemExit(f"Required local dependency missing: sentence-transformers for {name}. Original error: {exc}") from exc
    try:
        return SentenceTransformer(name, local_files_only=True)
    except Exception as exc:
        raise SystemExit(f"Required local embedding model unavailable or not cached locally: {name}. Original error: {exc}") from exc


def encode(model, text: str) -> list[float]:
    try:
        vector = model.encode([text], normalize_embeddings=True)[0]
    except TypeError:
        vector = model.encode([text])[0]
    return [float(x) for x in vector]


def reward(ep: dict) -> float:
    if ep.get("reward") is not None:
        return float(ep["reward"])
    outcome = str(ep.get("outcome", "")).lower()
    if any(w in outcome for w in ("success", "completed", "pass", "accepted")):
        return 1.0
    if any(w in outcome for w in ("partial", "mixed")):
        return 0.5
    if any(w in outcome for w in ("fail", "reject", "error")):
        return 0.0
    return 0.25


def trace(value: Any) -> list[Any]:
    if not value:
        return []
    if isinstance(value, str):
        return [part.strip() for part in value.split(",") if part.strip()]
    return value if isinstance(value, list) else [value]


def proc_id(item: Any) -> str:
    if isinstance(item, dict):
        return str(item.get("id") or item.get("node_id") or slug(item.get("label") or item.get("summary") or stringify(item)))
    return str(item) if str(item).startswith("proc_") else slug(str(item))


def proc_summary(item: Any) -> str:
    if isinstance(item, dict):
        return str(item.get("summary") or item.get("label") or item.get("name") or item.get("id") or stringify(item))
    return str(item)


def ensure_node(graph: dict, item: Any, evidence_ref: str) -> str:
    node_id = proc_id(item)
    for node in graph.setdefault("nodes", []):
        if node.get("id") == node_id:
            node["observed_count"] = int(node.get("observed_count") or 0) + 1
            return node_id
    graph["nodes"].append({"id": node_id, "label": proc_summary(item), "summary": proc_summary(item), "observed_count": 1, "evidence_refs": [evidence_ref] if evidence_ref else [], "reliability": "observed"})
    return node_id


def edge_id(a: str, b: str) -> str:
    return f"edge_{a.removeprefix('proc_')}_to_{b.removeprefix('proc_')}"[:120]


def vec_add(existing: list[float], vector: list[float], weight: float) -> list[float]:
    if not existing:
        existing = [0.0] * len(vector)
    return [float(a) + weight * float(b) for a, b in zip(existing, vector)]


def update_edge(graph: dict, a: str, b: str, ep: dict, task_vector: list[float], r: float) -> None:
    eid = edge_id(a, b)
    edge = next((e for e in graph.setdefault("edges", []) if e.get("id") == eid), None)
    if edge is None:
        edge = {"id": eid, "from": a, "to": b, "observed_count": 0, "success_count": 0, "failure_count": 0, "reward_sum": 0.0, "mean_reward": 0.0, "reliability_weight_sum": 0.0, "reliability_vector_sum": [], "evidence_refs": []}
        graph["edges"].append(edge)
    edge["observed_count"] = int(edge.get("observed_count") or 0) + 1
    edge["success_count"] = int(edge.get("success_count") or 0) + (1 if r >= 0.75 else 0)
    edge["failure_count"] = int(edge.get("failure_count") or 0) + (1 if r <= 0.25 else 0)
    edge["reward_sum"] = float(edge.get("reward_sum") or 0.0) + r
    edge["mean_reward"] = edge["reward_sum"] / max(edge["observed_count"], 1)
    if abs(r) > 0:
        edge["reliability_vector_sum"] = vec_add(edge.get("reliability_vector_sum") or [], task_vector, abs(r))
        edge["reliability_weight_sum"] = float(edge.get("reliability_weight_sum") or 0.0) + abs(r)
    edge["reliability_note"] = f"observed_count={edge['observed_count']}; mean_reward={edge['mean_reward']:.3f}"
    ref = ep.get("evidence_ref") or ep.get("id")
    if ref and ref not in edge.setdefault("evidence_refs", []):
        edge["evidence_refs"].append(ref)


def add_failures(graph: dict, ep: dict, r: float) -> None:
    existing = {f.get("id") for f in graph.setdefault("failure_patterns", [])}
    items = list(ep.get("failure_patterns") or [])
    if r < 0.75 and ep.get("failure_suffix"):
        items.append({"pattern": "failure_suffix", "context": stringify(ep.get("failure_suffix")), "avoidance": "Review this suffix before repeating the same transition."})
    for item in items:
        record = dict(item) if isinstance(item, dict) else {"pattern": str(item)}
        fid = record.get("id") or slug(record.get("pattern") or record.get("context") or stringify(record), "fail")
        if fid in existing:
            continue
        record.setdefault("id", fid)
        record.setdefault("context", ep.get("request_summary"))
        record.setdefault("evidence_ref", ep.get("evidence_ref") or ep.get("id"))
        graph["failure_patterns"].append(record)
        existing.add(fid)


def select_episodes(graph: dict, episode_id: str | None, all_episodes: bool) -> list[dict]:
    episodes = graph.get("episodes", [])
    if all_episodes:
        return episodes
    if episode_id:
        selected = [ep for ep in episodes if ep.get("id") == episode_id]
        if not selected:
            raise SystemExit(f"Episode not found: {episode_id}")
        return selected
    return episodes[-1:] if episodes else []


def refine(graph: dict, ep: dict, model) -> dict:
    r = reward(ep)
    text = " | ".join(str(x) for x in [ep.get("task_family"), ep.get("request_summary"), ep.get("validation_signal")] if x)
    task_vector = encode(model, text)
    ref = ep.get("evidence_ref") or ep.get("id")
    for item in trace(ep.get("procedure_candidates")):
        ensure_node(graph, item, ref)
    steps = trace(ep.get("productive_prefix")) or trace(ep.get("executed_trace")) or trace(ep.get("procedures_used")) or trace(ep.get("planned_trace"))
    ids = [ensure_node(graph, item, ref) for item in steps]
    for a, b in zip(ids, ids[1:]):
        update_edge(graph, a, b, ep, task_vector, r)
    add_failures(graph, ep, r)
    ep["refined"] = True
    ep["refinement_reward"] = r
    return {"episode_id": ep.get("id"), "nodes": len(ids), "edges": max(len(ids)-1, 0), "reward": r}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("graph", help="Path to references/procedure-graph.json")
    parser.add_argument("--episode-id", help="Episode id to refine; defaults to latest")
    parser.add_argument("--all", action="store_true", help="Refine all episodes")
    parser.add_argument("--embedding-model", default="sentence-transformers/all-MiniLM-L6-v2", help="Required local SentenceTransformers model")
    parser.add_argument("--json", action="store_true", help="Emit JSON summary")
    args = parser.parse_args()
    path = Path(args.graph)
    graph = json.loads(path.read_text(encoding="utf-8-sig"))
    model = load_model(args.embedding_model)
    summaries = [refine(graph, ep, model) for ep in select_episodes(graph, args.episode_id, args.all)]
    graph.setdefault("refinement_policy", {"method": "local_trace_reward_reliability", "embedding_model": args.embedding_model, "api_calls_required": False})
    path.write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps({"refined": summaries}, indent=2))
    else:
        for s in summaries:
            print(f"refined={s['episode_id']} nodes={s['nodes']} edges={s['edges']} reward={s['reward']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''



def read_skill_name(skill_md: Path) -> str:
    text = skill_md.read_text(encoding="utf-8-sig")
    match = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return skill_md.parent.name
    for line in match.group(1).splitlines():
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip().strip('"\'')
    return skill_md.parent.name


def procedure_memory_text(skill_name: str) -> str:
    return f"""# Procedural Memory

This file supports a ProPlay-inspired, Codex-native retrieve-preplay-execute-capture-refine loop for `${skill_name}`.

## Retrieval

Retrieval requires local embeddings and combines 75% normalized RRF score with 25% normalized dense similarity. Before preplay, run:

```bash
python scripts/retrieve_memory.py references/procedure-graph.json --query "Current task summary" --top-k 8 --inject-k 3
```

The default embedding model is `sentence-transformers/all-MiniLM-L6-v2`. If the dependency or model is unavailable, fix the local embedding setup before relying on this skill. Retrieval and refinement should fail clearly rather than falling back to API calls.

## Capture Policy

Default mode is `auto`. Before the final response, record a compact episode when the run contains reusable procedural signal.

Do not skip capture unless the user explicitly confirms skipping for this run. If capture seems low-signal, sensitive, or evaluation-contaminating, ask for explicit skip confirmation; otherwise record a minimal sanitized episode.

Every final answer should include a receipt:

```text
Procedural memory: recorded episode_YYYYMMDD_short_slug.
```

or:

```text
Procedural memory: skipped by explicit user confirmation because <specific reason>.
```

## Preplay

1. Identify the current task family.
2. Run required embedding+RRF retrieval and review similar failures plus relevant transitions.
3. Draft a short task-specific procedural plan.
4. Treat that plan as soft guidance. User instructions and fresh evidence override stale memory.

## Execute

Use the target skill's normal workflow. Let procedural memory guide sequencing and checks, but do not skip domain-specific instructions, validation gates, or tool requirements already present in `SKILL.md`.

## Capture

Before the final response, create a compact episode and run:

```bash
python scripts/record_episode.py references/procedure-graph.json --task-family example-family --request-summary "Compact task summary" --outcome completed --reward 1.0 --planned-trace proc_research,proc_draft --executed-trace proc_research,proc_draft,proc_validate --lesson "Reusable lesson from this run" --evidence-ref current-thread
```

Add `--procedure proc_example` for each procedure used and `--failure-pattern fail_example` for each reusable failure pattern. Prefer `--executed-trace` over planned trace when they differ. For richer episodes, pass `--episode-json` with `planned_trace`, `executed_trace`, `productive_prefix`, `failure_suffix`, `procedure_candidates`, `failure_patterns`, `validation_signal`, and `environment_observations`.

Do not store full transcripts, hidden benchmark answers, or unnecessary personal data.

## Refine

After recording, run:

```bash
python scripts/refine_graph.py references/procedure-graph.json --episode-id episode_id_from_record_episode
```

The refiner uses local sentence-transformer embeddings to add missing procedure nodes, update observed edges from the executed trace or productive prefix, maintain reward-weighted transition reliability vectors, and add compact failure patterns from failed suffixes. It must not call paid APIs.

## Training Instructions

```text
Use ${skill_name} on this task. Run required embedding+RRF procedural-memory retrieval before preplay and auto-record a compact episode unless I explicitly confirm skipping.
```

```text
For this run, do not record procedural memory. Treat this as explicit confirmation to skip because it is held-out evaluation.
```

## Contamination Rules

Keep held-out prompts, evaluator rubrics, and hidden expected answers out of memory until they are no longer needed for clean evaluation. User-provided "do not record" is explicit skip confirmation.
"""


def insert_section(skill_md: Path) -> bool:
    text = skill_md.read_text(encoding="utf-8-sig")
    if "## Procedural Memory" in text:
        return False
    frontmatter = re.match(r"(---\s*\n.*?\n---\s*\n)", text, re.DOTALL)
    insert_at = frontmatter.end() if frontmatter else 0
    heading = re.search(r"^# .+$", text[insert_at:], re.MULTILINE)
    if heading:
        insert_at += heading.end()
    new_text = text[:insert_at].rstrip() + "\n\n" + PROCEDURAL_SECTION.strip() + "\n\n" + text[insert_at:].lstrip()
    skill_md.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target_skill", help="Path to the target skill directory")
    parser.add_argument("--patch-skill", action="store_true", help="Insert a Procedural Memory section into SKILL.md")
    parser.add_argument("--force", action="store_true", help="Overwrite existing procedure-memory files")
    args = parser.parse_args()

    target = Path(args.target_skill).expanduser().resolve()
    skill_md = target / "SKILL.md"
    if not skill_md.exists():
        raise SystemExit(f"SKILL.md not found: {skill_md}")

    skill_name = read_skill_name(skill_md)
    references = target / "references"
    scripts = target / "scripts"
    references.mkdir(exist_ok=True)
    scripts.mkdir(exist_ok=True)

    memory_md = references / "procedure-memory.md"
    graph_json = references / "procedure-graph.json"
    retrieve_script = scripts / "retrieve_memory.py"
    record_script = scripts / "record_episode.py"
    refine_script = scripts / "refine_graph.py"

    if args.force or not memory_md.exists():
        memory_md.write_text(procedure_memory_text(skill_name), encoding="utf-8")

    if args.force or not graph_json.exists():
        graph = {
            "schema_version": 1,
            "skill": skill_name,
            "capture_policy": {
                "mode": "auto",
                "before_final_required": True,
                "receipt_required": True,
                "skip_requires_confirmation": True,
                "sensitive_data": "summarize_or_confirm_skip",
            },
            "retrieval_policy": {
                "method": "hybrid_rrf_dense_reliability",
                "rrf_weight": 0.75,
                "dense_weight": 0.25,
                "dense_required": True,
                "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
                "default_top_k": 8,
                "inject_k": 3,
                "rrf_k": 60,
                "rankers": ["lexical", "procedure_overlap", "failure_pattern_match"],
                "reliability_weight": 0.15,
            },
            "nodes": [],
            "edges": [],
            "episodes": [],
            "failure_patterns": [],
            "environment_interfaces": [],
            "refinement_policy": {
                "method": "local_trace_reward_reliability",
                "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
                "api_calls_required": False,
            },
        }
        graph_json.write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")

    if args.force or not retrieve_script.exists():
        retrieve_script.write_text(RETRIEVE_MEMORY_SCRIPT, encoding="utf-8")
    if args.force or not record_script.exists():
        record_script.write_text(RECORD_EPISODE_SCRIPT, encoding="utf-8")
    if args.force or not refine_script.exists():
        refine_script.write_text(REFINE_GRAPH_SCRIPT, encoding="utf-8")

    patched = insert_section(skill_md) if args.patch_skill else False

    print(f"target={target}")
    print(f"skill={skill_name}")
    print(f"memory={memory_md}")
    print(f"graph={graph_json}")
    print(f"retrieve_script={retrieve_script}")
    print(f"record_script={record_script}")
    print(f"refine_script={refine_script}")
    print("retrieval_method=hybrid_rrf_dense_reliability")
    print("embedding_model=sentence-transformers/all-MiniLM-L6-v2")
    print("capture_mode=auto")
    print("refinement_method=local_trace_reward_reliability")
    print("skip_requires_confirmation=true")
    print(f"patched_skill={str(patched).lower()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())