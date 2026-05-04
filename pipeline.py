from agents import build_reader_agent , build_search_agent , writer_chain , critic_chain

def run_research_pipeline(topic : str) -> dict:

    state = {}

    # Search Agent Working
    print("\n" + "="*40)
    print("Step 1  = Search Agent in Working .. ")
    print("\n" + "="*40)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages" : [("user", f"Find recent, reliable and detailed information about: {topic}")]

    })

    state["search_results"] = search_result['messages'][-1].content

    print("\n search result ", state['search_results'])


    # Step 2 = Reader Agent 
    print("\n" + "="*40)
    print("Step 2  = Reader Agent in Scraping Top Resources .. ")
    print("\n" + "="*40)

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search result about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content, \n\n"
            f"Search Results: \n{state['search_results'][:800]}")]
    })

    state['scraped_content'] = reader_result['messages'][-1].content

    print("\n Scrapped content\n", state['scraped_content'])


    # Step 3 - Writer Chain
    print("\n" + "="*40)
    print("Step 3  =  Writer is Drafting the Report .. ")
    print("\n" + "="*40)

    research_combined = (
        f"Search Results: \n {state['search_results']} \n\n"
        f"Detailed Scrapped Content : \n {state['scraped_content']}"
    )

    state['report'] = writer_chain.invoke({
        "topic" : topic,
        "research" : research_combined
    })

    print("\n Final Report \n" , state['report'])


    # Critic Report 
    print("\n" + "="*40)
    print("Step 4  =  Critic is Reviewing Report .. ")
    print("\n" + "="*40)

    state['feedback'] = critic_chain.invoke({
        "report" : state["report"]
    })

    print("\n critic report \n" , state["feedback"])

    return state


if __name__ == "__main__":
    topic = input("\n Enter Research topic : ")
    run_research_pipeline(topic)


