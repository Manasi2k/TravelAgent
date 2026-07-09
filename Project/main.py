import os
from dotenv import load_dotenv
load_dotenv()
from langchain.chat_models import init_chat_model
from langchain_groq import ChatGroq

#os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")


import streamlit as st
model=init_chat_model("groq:llama-3.3-70b-versatile")
groq_key = st.secrets["GROQ_API_KEY"]

from typing import TypedDict,Annotated
from typing_extensions import NotRequired
from langgraph.graph import StateGraph,START,END
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage,AnyMessage
from langgraph.checkpoint.postgres import PostgresSaver
import psycopg
import operator
#DATABASE_URL=os.getenv("DATABASE_URL")

#
import streamlit as stt
def get_connection():

   # DATABASE_URL = os.getenv("DATABASE_URL")
    DATABASE_URL = stt.secrets["DATABASE_URL"]
    return psycopg.connect(
        DATABASE_URL,
        autocommit=True
    )


from Tools.Flight_Search import flight_search
from Tools.Tavily_Search import tavily_search


#Create State

class TravelState(TypedDict):
    messages:Annotated[list[AnyMessage],operator.add]
    user_query:str
    #"Whenever someone updates messages,don't replace the old list.
    #  Add the new messages to the existing list."
    flight_result:NotRequired[str]
    hotel_result:NotRequired[str]
    itinerary_result:NotRequired[str]
    llm_calls:NotRequired[int]


#Create Flight Agent

def Flight_Agent(state:TravelState):
    query=state["user_query"]
    flight_data=flight_search(query)
    return{
        "flight_result":flight_data,
        "messages":[AIMessage(content=f"Flight Details Fetched!")],
        "llm_calls":state.get("llm_calls",0)+1
    }

def Hotel_Agent(state:TravelState):
    query=state["user_query"]
    hotel_data=query
    return{
        "hotel_result":hotel_data,
        "messages":[AIMessage(content=f"Hotel Data Fetched!")],
        "llm_calls":state.get("llm_calls",0)+1
    }

def Itinerary_Agent(state:TravelState):
    prompt=f"""Create a travel itimeary.
    User query:{state.get('user_query',"")}
    Flight Result:{state.get('flight_result',"")}
    Hotel Result:{state.get('hotel_result',"")} 
    itinerary Result:{state.get('itinerary_result',"")}]
    """

    response=model.invoke([SystemMessage(content="You are helpful expert travel guide agent"),
                           HumanMessage(content=prompt)])
    

    return {
        "itinerary_result":response.content,
        "messages":[response],
        "llm_calls":state.get("llm_calls",0)+1
    }


def Final_Agent(state:TravelState):
    final_prompt=f"""Generate final travel plan.
    Flights: {state['flight_result']}
    Hotels: {state['hotel_result']}
    itinerary: {state['itinerary_result']}
    """

    final_response=model.invoke([HumanMessage(content=final_prompt)])

    return {
        "messages":[final_response],
        "llm_calls":state.get("llm_calls",0)+1

    }

graph=StateGraph(TravelState)

graph.add_node("Flight_Agent",Flight_Agent)
graph.add_node("Hotel_Agent",Hotel_Agent)
graph.add_node("Itinerary_Agent",Itinerary_Agent)
graph.add_node("Final_Agent",Final_Agent)

graph.add_edge(START,"Flight_Agent")
graph.add_edge("Flight_Agent","Hotel_Agent")
graph.add_edge("Hotel_Agent","Itinerary_Agent")
graph.add_edge("Itinerary_Agent","Final_Agent")
graph.add_edge("Final_Agent",END)



#connectSQL=psycopg.connect(DATABASE_URL,autocommit=True)

connectSQL = get_connection()
checkpointer=PostgresSaver(connectSQL)
checkpointer.setup()

app=graph.compile(checkpointer=checkpointer)



#"Run this code only when this file is executed directly,
#  not when it is imported into another file."

if __name__== "__main__":
    config={"configurable":{"thread_id":"admin_manasi"}}

    user_input=input("Enter travel request: ")

    
    result= app.invoke({
        "messages":[HumanMessage(content=user_input)],
        "user_query":user_input,
        "flight_result":"",
        "hotel_result":"",
        "itinerary_result":"",
        "llm_calls":0
    },config=config)


    print("\nFINAL RESPONSE : \n")

    
    for m in result["messages"]:
        print(m.content)

                                





