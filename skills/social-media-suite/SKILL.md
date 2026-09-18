---
name: social-media-suite
description: |
  Unified Social Media Engineering & Distribution Suite combining social graph ranking algorithms (warm intro scoring, bridge metrics), multi-platform agent publishing via SocialClaw (X, LinkedIn, TikTok, Instagram, Reddit, Discord), and pixel-perfect social preview cards (Reddit vote cards, Spotify now-playing cards, X/Twitter metric cards).
triggers:
  - "social media"
  - "social publisher"
  - "social graph"
  - "social cards"
  - "x card"
  - "reddit card"
  - "spotify card"
license: MIT
metadata:
  origin: ECC
---

# Social Media Suite & Network Intelligence

Comprehensive social media architecture uniting social graph ranking mathematics, autonomous cross-platform publishing pipelines, and pixel-accurate interactive preview cards.

---

## 1. Social Graph Ranking & Network Math

Graph-based scoring for warm introductions and influence discovery across professional networks (X / LinkedIn / Farcaster):

### Scoring Formula
$$\text{Score}(u, v) = w_1 \cdot \text{InteractionFreq}(u, v) + w_2 \cdot \text{MutualOverlap}(u, v) + w_3 \cdot \text{BridgeCentrality}(v)$$

```python
# ponytail: Social Graph Warm Intro Ranker - single-pass weighted adjacency scoring
from typing import Dict, List, Tuple

def rank_warm_intros(
    network_graph: Dict[str, Dict[str, float]], 
    target_user: str, 
    my_user_id: str
) -> List[Tuple[str, float]]:
    """
    Ranks direct 1st-degree connections by path strength to reach target_user.
    """
    candidates = []
    my_connections = network_graph.get(my_user_id, {})
    target_connections = network_graph.get(target_user, {})

    for connector_id, direct_weight in my_connections.items():
        if connector_id in target_connections:
            target_weight = target_connections[connector_id]
            # Geometric mean of mutual path weights
            path_score = (direct_weight * target_weight) ** 0.5
            candidates.append((connector_id, round(path_score, 4)))

    candidates.sort(key=lambda x: x[1], reverse=True)
    return candidates
```

---

## 2. Multi-Platform Autonomous Publishing

Automate scheduling and distribution across 13+ social platforms through unified workspace APIs (SocialClaw / Buffer / Custom Webhooks).

### Capabilities
- **Cross-Posting**: Publish to X, LinkedIn, Instagram, TikTok, Discord, Telegram, and Reddit simultaneously.
- **Campaign Validation**: Pre-flight validation of character limits, image aspect ratios (16:9 for X/LinkedIn, 9:16 for TikTok/Reels), and video encoding standards (H.264, AAC).
- **Delivery Monitoring**: Ingest webhooks to track post status, engagement anomalies, and reply sentiment.

---

## 3. High-Fidelity Social Preview Cards

### Reddit Post Card Component
Realistic Reddit dark-mode card with interactive upvote/downvote rail and comment counts:

```tsx
// ponytail: Reddit Post Card Template
export function RedditPostCard({
  subreddit,
  author,
  timeAgo,
  title,
  body,
  upvotes,
  comments,
}: {
  subreddit: string;
  author: string;
  timeAgo: string;
  title: string;
  body: string;
  upvotes: number;
  comments: number;
}) {
  return (
    <div className="flex bg-[#1a1a1b] text-[#d7dadc] border border-[#343536] rounded-md max-w-xl overflow-hidden font-sans">
      <div className="w-10 bg-[#151516] flex flex-col items-center py-2 gap-1 select-none">
        <button className="text-neutral-400 hover:text-orange-500">▲</button>
        <span className="text-xs font-bold">{upvotes >= 1000 ? `${(upvotes / 1000).toFixed(1)}k` : upvotes}</span>
        <button className="text-neutral-400 hover:text-blue-500">▼</button>
      </div>
      <div className="flex-1 p-3">
        <div className="text-xs text-neutral-400 mb-1">
          <span className="font-bold text-white hover:underline cursor-pointer">r/{subreddit}</span> • Posted by u/{author} {timeAgo}
        </div>
        <h3 className="text-base font-semibold text-white mb-2">{title}</h3>
        <p className="text-sm text-neutral-300 line-clamp-3 mb-3">{body}</p>
        <div className="flex items-center gap-4 text-xs text-neutral-400 font-bold">
          <span>💬 {comments} Comments</span>
          <span>↗ Share</span>
          <span>💾 Save</span>
        </div>
      </div>
    </div>
  );
}
```

### Spotify Now-Playing Card Component
Dark aesthetic music widget with waveform progress and track controls.

### X (Twitter) Post Card Component
Clean X dark-mode card with verified badge, tweet text formatting, media attachment, and real-time engagement counters (Likes, Reposts, Views).
