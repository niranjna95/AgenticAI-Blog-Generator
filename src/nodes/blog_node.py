from src.states.blogstate import BlogState
class BlogNode:
    """A class to represent he blog node"""
    def __init__(self, llm):
        self.llm=llm
    
    def title_creation(self, state: BlogState):
        """
        Generates a blog title based on the given topic.
        """
        if "topic" in state and state["topic"]:
            prompt="""You are an expert blog content writer. Generate ONLY a single-line catchy and SEO-friendly blog title for the following topic. Respond with ONLY the title, nothing else:
            Topic: {topic}"""
            system_message = prompt.format(topic=state["topic"])
            print(system_message)
            response = self.llm.invoke(system_message)
            # Extract only the first line and remove any markdown formatting
            title = response.content.strip().split('\n')[0].strip('*#').strip()
            return {"blog":{"title":title}}
        
    def content_generation(self, state:BlogState):
        if "topic" in state and state["topic"]:
            system_prompt="""You are expert blog writer. Use Markdown formatting.
            Generate a detailed blog content with detailed breakdown for the {topic}"""
            system_message = system_prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog":{"title":state['blog']['title'], "content":response.content}}

