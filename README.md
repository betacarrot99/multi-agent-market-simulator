# Multi-Agent Market Simulator: AI-Driven Fixed Income Price Discovery

**A sophisticated agent-based model that simulates realistic market dynamics using specialized AI agents representing different market participants.**

---


## What I Created

I built a **hierarchical multi-agent simulation** with three architectural layers:

### Layer 1: Research Intelligence

**Seven Regional Research Agents** (US, Euro, JPY, CHF, AUD, NZD, plus orchestrator) extract macro forecasts from JPMorgan research PDFs. Each specializes in regional data: rates, inflation, growth projections. The **Orchestrator Agent** coordinates parallel extraction and consolidates findings.

A **Scenario Agent** then generates logically consistent bull/bear/base case macro paths, interpolating from research forecasts to create realistic forward-looking scenarios.

### Layer 2: Market Participant Simulation

Five specialized agents represent real market archetypes, each with distinct behavioral rules:

**1. Central Bank Agent**  
Acts every 10 days following a data-dependent policy reaction function. If inflation is high and growth strong, it leans hawkish. If credit stress emerges, it overrides baseline logic and pivots dovish immediately to protect financial stability. This mirrors real central bank behavior: infrequent but systematic.

**2. Commercial Bank Agent**  
The market's liquidity provider and price discovery mechanism. Quotes bid/ask spreads continuously, managing inventory within regulatory limits. In calm markets, spreads are tight. When volatility spikes or hedge funds dump positions, it widens spreads and reduces size. This agent's quotes become the **observable market price**.

**3. Leveraged Fund Agent**  
A global macro hedge fund trading every 3 days. It exploits valuation gaps and cross-asset mispricings with leverage. Crucially, it faces **margin constraints**: if positions move against it, forced liquidations override all strategy logic. This creates realistic crisis dynamics.

**4. Long-Term Investor Agent**  
Represents pension funds and sovereign wealth funds. Rebalances every 5 days based on fair value vs. market price. Must stay invested, providing a stabilizing force. When prices overshoot, it systematically buys the dip. When prices undershoot, it trims exposure.

**5. Momentum Trader Agent**  
A purely systematic CTA algorithm reacting every tick to price trends and volatility. It has **zero fundamental awareness**: doesn't care about Fed policy or macro data. It simply amplifies existing trends mechanically, often pushing prices to extremes before reversing.

These five agents run in **ParallelAgent** mode to simulate simultaneous decision-making during each market period. Their collective actions feed into the commercial bank's bid/ask quotes.

### Layer 3: Validation and Refinement

**Trading Loop:** A `LoopAgent` iterates the simulation across multiple time periods, with agents reacting to evolving conditions and each other's actions.

**Critic Agent:** Validates simulation outputs for three criteria:
- **Macro consistency:** All data must align with JPM research (no hallucinated numbers)
- **Bond math correctness:** Yield up must mean price down, spread widening must reduce price
- **Agent interaction realism:** Central bank timing, margin call mechanics, dealer spread logic must follow rules

**Refiner Agent:** If the critic finds issues, the refiner incorporates corrections and regenerates output. If approved, it passes through unchanged. Final output is always clean, professional analysis free of internal system references.

**Extraction Agent:** Pulls the final bid/ask price path and key metrics for analysis.

The **Root Agent** (`SequentialAgent`) orchestrates the entire workflow: Research → Scenarios → Market Simulation → Critique → Refinement → Extraction.

---


## The Build

**Technologies:**
- **Google ADK (Agentic Development Kit):** Framework for LlmAgent, SequentialAgent, ParallelAgent, LoopAgent
- **Gemini 2.5 Flash Lite:** LLM backend for all agents
- **PyPDF2:** Research report extraction
- **Python:** Simulation logic and orchestration


