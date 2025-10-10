from agent_components.game_components import Goal

file_management_goal = Goal(
    priority=1,
    name="File Management",
    description="""Manage files in the current directory by :
    1. Listing files when needed.
    2. Reading file contents when needed.
    3. Searching within files when information is required.
    4. Provide helpful explanations about file contents.
    """
    )

goals = [
        Goal(
          priority=1, 
          name="Gather Information", 
          description="Read each file in the project"),
        Goal(
          priority=1, 
          name="Terminate", 
          description="Call the terminate call when you have read all the files "
                      "and provide the content of the README in the terminate message")
    ]