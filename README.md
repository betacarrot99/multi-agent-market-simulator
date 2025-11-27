# Multi-Agent Market Simulator: AI-Driven Fixed Income Price Discovery

**A sophisticated agent-based model that simulates realistic market dynamics using specialized AI agents representing different market participants.**

---

## Problem Statement

Fixed income markets are fundamentally opaque. Unlike equities traded on centralized exchanges, bond prices emerge from decentralized dealer networks and institutional negotiations. Understanding price evolution requires modeling complex interactions between heterogeneous market participants: central banks setting policy, commercial banks providing liquidity, hedge funds exploiting mispricings, pension funds rebalancing portfolios, and algorithmic traders amplifying trends.

Traditional financial models use mathematical equations assuming rational, homogeneous actors. But real markets are emergent systems where price discovery arises from participants with conflicting mandates, timeframes, and constraints. When the Fed signals dovishness while hedge funds are overleveraged, the cascading price effects are impossible to capture with closed-form equations.

For fixed income portfolio managers, simulating "what if" scenarios (how would 10Y Treasury prices evolve under specific macro conditions and participant positioning) is invaluable for risk management and trade positioning. This is the problem I set out to solve.

---

## Why Agents?

Agents are the perfect solution because bond markets are fundamentally **multi-participant systems** where behavior is heterogeneous, timing is asynchronous, and outcomes emerge from interactions:

**Heterogeneous Decision-Making:** Each participant operates under distinct rules. A pension fund rebalances every 5 days based on valuation. A CTA flips positions every tick based purely on momentum. A central bank acts every 10 days on economic data. Agents naturally model this diversity through specialized instruction sets.

**Temporal Dynamics:** Market participants don't act simultaneously. Central banks have fixed meeting schedules. Commercial banks quote continuously. Hedge funds trade on 3-day cycles. The `SequentialAgent` and `ParallelAgent` architectures mirror these real-world timing patterns.

**Emergent Feedback Loops:** When momentum traders push prices beyond fair value, long-term investors step in to fade the move. When hedge funds hit margin calls, forced liquidations trigger commercial bank spread widening, accelerating price moves. These cascades only emerge through agent interaction; they can't be pre-programmed.

**Research Integration:** Rather than hallucinating data, agents ground decisions in real JPMorgan research reports extracted via PDF parsing, ensuring realistic macro scenarios.

**Iterative Validation:** A `LoopAgent` with critic and refiner agents ensures logical consistency, validating that "yield up = price down" and catching contradictions before finalizing outputs.

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

## How It Works: A Demo

**User Query:** *"Forecast 10Y Treasury price evolution using US information."*

**Execution Flow:**

1. **Research agents** extract US rate forecasts, inflation expectations, and GDP growth from JPM PDFs. In the submission, the PDFs are excluded due to JPM's T&C.
2. **Scenario agent** generates three macro paths (bull/bear/base)
3. **Market simulation begins** with commercial bank setting initial quotes at 101.50 bid / 101.65 ask
4. **Iteration 1:** Central bank holds rates steady. Hedge fund identifies undervaluation and buys aggressively. Momentum trader detects uptrend and joins. Commercial bank narrows spread to 101.60/101.70 as liquidity improves.
5. **Iteration 2:** Price rises to 102.20/102.35. Long-term investor's fair value model shows overvaluation, so it begins trimming exposure. Momentum trader reverses on trend break.
6. **Iteration 3:** Hedge fund's leveraged long position hits margin threshold, triggering **forced liquidation**. Commercial bank sees massive sell flow, widens spread to 102.00/102.50 to protect inventory.
7. **Iteration 4:** Long-term investor steps in as value buyer at lower prices. Market stabilizes at 101.80/102.00.
8. **Critic validates:** Confirms price fell as hedge fund liquidated, spread widening matched volatility spike, agent timing followed prescribed rules
9. **Refiner outputs:** Clean narrative with price path evolution
10. **Extraction agent summarizes:** Final bid 101.80, ask 102.00, spread widened from 15bps to 50bps during stress

Due to token and time constraint, I ran this simulation **5 times** to generate a distribution of outcomes, capturing path dependency and stochastic variation. In an ideal scenario, we need to run the simulation at least 30 times based on Central Limit Theorem to build a valid distribution.

---

## The Build

**Technologies:**
- **Google ADK (Agentic Development Kit):** Framework for LlmAgent, SequentialAgent, ParallelAgent, LoopAgent
- **Gemini 2.5 Flash Lite:** LLM backend for all agents
- **PyPDF2:** Research report extraction
- **Python:** Simulation logic and orchestration

**Implementation:**

First, I built the research pipeline. The function `read_pdf_content()` extracts text from PDFs, while `read_all_pdfs_in_folder()` batch-processes the entire database. Extracted content is injected into agent system prompts as grounded context.

Next, I designed detailed behavioral prompts for each agent. Central bank uses Taylor-rule logic with crisis overrides. Commercial bank adjusts spreads dynamically based on volatility and order flow. Hedge fund has explicit margin thresholds. Each agent can access other agents' outputs: commercial bank sees hedge fund positioning, long-term investor observes dealer spreads.

The orchestration layer chains agents appropriately. `ParallelAgent` simulates simultaneous market participant actions. `SequentialAgent` enforces workflow order. `LoopAgent` enables iterative simulation with exit conditions.

The validation layer ensures quality. Critic agent validates bond math and logical consistency, while refiner agent produces clean professional output. Finally I wrapped everything in **Streamlit** application for easy user interaction.



---

## If I Had More Time

**Network contagion modeling:** Add balance sheet interconnections to model how stress propagates through dealer networks when one participant fails.

**Real-time data integration:** Replace static PDFs with live Bloomberg Terminal API feeds for actual tick-by-tick simulation.

**Cross-asset dynamics:** Expand to model FX, equity, and credit simultaneously, capturing spillover effects.

**ML-based calibration:** Train agent parameters on historical data to improve behavioral realism.

**Visualization dashboard:** Build Streamlit interface showing live agent positions, price evolution, interaction networks, and spread dynamics.

**Backtesting:** Validate agent behavior against historical crises (2008, COVID, 2022 rate shock).

**Derivatives layer:** Add options, futures, and CDS trading with gamma hedging dynamics.

**Regulatory constraints:** Encode Basel III requirements and stress test scenarios.

**Monte Carlo ensembles:** Run 1000+ simulations in parallel, displaying probability distributions and Value-at-Risk metrics via Streamlit histograms and confidence bands.

This project demonstrates **agentic AI's power for financial simulation**, moving beyond static models to capture the emergent, interactive, path-dependent nature of real markets. It's a foundation for next-generation institutional risk management.
