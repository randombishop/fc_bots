# Building Reliable AI Agents: A Farcaster Native Framework

## The Challenge of Building AI Agents

When I started building my bot on Farcaster, I found it pretty easy in the beginning, and didn't even need a framework. 
Coming from years of classic software enginnering, LLMs feel so powerful, after defining some data access functions, most of the logic doesn't need to be written in python anymore, just tell the LLM what you want and it will figure out which tools to use and get you an answer.

Many AI solutions out there, including leading ones like OpenAI Assistants, advertise that the sky is the limit now: you just need to plug in your tools and the LLM will know how to use them to respond to any user request.

But the truth is, I found that it only works with a limited set of tools, and only if they are very simple and independent. For example, add a tool for the weather and another one for the stock prices, and the agent will properly trigger them and provide good answers that require a weather forecast or some stock price. But if you plug-in 10 or more different tools, it becomes a mess. The agent gets confused with too many options and starts calling them not like a programmer would do, 
but like someone who never used them before would make very approximate decisions on how to write a program, learn by trial and error, and at some point go so far on a wrong path that they don't even remember what they were trying to achieve in the first place.

As I started adding more tools to my agent library: searching casts with a keyword, with a search phrase, selecting a user, describing their PFP and casts, generating an avatar, etc. The agent became more and more unreliable.

Here is a simple example: my agent has access to multiple tools to search for casts on Farcaster social media platform, plus multiple AIs, 
plus the ability to query some datasets directly from Dune Analytics.

Someone asks: "How many Brazilians do we have on Farcaster?" 
The correct plan is to use the MakeUserStatsSQLQuery tool followed by GetUserStats tool; but when using the standard way of plugging tools to an LLM, it fails half of the time to respond with the correct answer.
Sometimes it tries forwarding the question to Perplexity AI, or searches for all casts with keyword brazil, and sometimes, even if it starts with MakeUserStatsSQLQuery, it realizes that the table doesn't have a country field, and won't go ahead with GetUserStats. Interestingly, it will be smart enough to use the portuguese language as a proxy to find brazilians because the prompt of MakeUserStatsSQLQuery instructs it to find workarounds when data is missing. But becausethe main prompt doesn't provide the same directive, it doesn't proceed afterwards.

One could propose an easy solution, why not simply add "it's ok to return an approximative number if you can't get the exact one." to all the prompts that will be used by the agent along its execution pipeline; but I learnt the hard way that such approach never converges. When provided with +50 tools, adding such hacks will improve one use-case and degrade another. And issues like this will keep raising and bloating the prompts with more and more edge cases.

So, in summary, even if frameworks like LangChain and AutoGPT lead the way and provide foundations for building AI agents, the core challenge remains: how do we reliably orchestrate LLMs to perform complex tasks while maintaining control over their behavior and ensuring reliable results?

## Current Approaches

Current approaches generally fall into two camps:

1. **Fully autonomous agents** like AutoGPT and BabyAGI that recursively use LLMs to plan and execute tasks. While flexible, they can be unpredictable and prone to hallucination.

2. **Structured frameworks** like LangChain that provide tools and patterns for building agents, but leave much of the orchestration logic to the developer.

Here are some useful resources on the topic:
- [Task-driven Autonomous Agent](https://github.com/yoheinakajima/babyagi) by Yohei Nakajima
- [The Rise and Potential of Large Language Model Based Agents](https://arxiv.org/abs/2309.07864) - A comprehensive survey
- [LangChain](https://github.com/langchain-ai/langchain) - The leading framework for building LLM applications


READ THE babyagi repo + the paper and write my personal comments...



## Building on LangChain's Foundation


This framework builds on LangChain's core concepts while adding structure specifically for social media bots. It uses LangChain's:
- Tool interface for defining atomic actions
- AgentExecutor for running tool chains
- BaseSingleActionAgent for custom agent logic

However, where it differs is in how tools are organized and orchestrated.

## A New Approach to Tool Organization

The framework organizes tools into logical phases that mirror how a human would approach social media interactions:

```
- init: Set up context and basic info
- intent: Determine what needs to be done
- plan: Design the response strategy
- parse: Extract key parameters
- fetch: Gather required data
- prepare: Transform data into presentable format
- compose: Create the actual posts
- check: Verify before posting
- memorize: Store relevant info for future use
```

This organization isn't just for code clarity - it fundamentally shapes how the agent operates.

## Three Modes of Operation

One of the most interesting aspects is how the framework supports three distinct modes:

1. **Blueprint Mode**: For when you need deterministic behavior. Tools run in a predefined sequence without LLM orchestration.

2. **Bot Mode**: A hybrid approach where an LLM detects intent but follows predefined plans for execution.

3. **Assistant Mode**: Full flexibility where the LLM plans and executes autonomously.

This allows developers to choose the right balance of control vs flexibility for each task.

## Focused LLM Usage

Each tool is designed to give the LLM a single, clear task with exactly the context it needs. For example, here's how the parse_user tool focuses the LLM:

```python
parse_user_instructions_template = """
#TASK:
You are @{{name}}, a bot programmed to analyze user data and perform actions such as analyzing, praising, roasting, etc.
Based on the provided conversation, who should your tools target?
You must only extract the user parameter so that you can set the user parameter.
Users typically start with @, but not always.
If the request is about self or uses a pronoun, study the context and instructions carefully to figure out the intended user.

#RESPONSE FORMAT:
{
  "user": ...
}
"""
```

The LLM gets clear instructions and a specific output format, making it much more reliable than if it had to handle multiple tasks at once.

## Similar Approaches

Several projects have explored similar ideas:
- [Microsoft's TaskMatrix](https://github.com/microsoft/TaskMatrix) uses a similar concept of tool categories
- [OpenAI's Assistants API](https://platform.openai.com/docs/assistants/overview) provides function calling with tools
- [Anthropic's Constitutional AI](https://www.anthropic.com/index/constitutional-ai-mild-optimization) explores ways to make AI behavior more reliable

However, this framework's focus on social media interactions and its three-mode approach appears unique.

## Pros, Cons, and Future Directions

### Pros:
- Clear organization of tools makes the system easy to understand and extend
- Three modes provide flexibility while maintaining control when needed
- Focused LLM prompts improve reliability

### Cons:
- More structured approach requires more upfront development
- May be overkill for simple use cases
- Still relies on LLM reliability for some tasks

### Future Improvements:
1. Add more sophisticated error handling and recovery
2. Implement better state management across tool chains
3. Create tools for automated testing of social media interactions
4. Explore ways to make the blueprint mode more dynamic while maintaining deterministic behavior

The framework shows how practical needs - in this case, building reliable social media bots - can drive innovation in AI agent architecture. By finding the right balance between structure and flexibility, it offers a promising approach for building more reliable AI agents. 