from jinja2 import FileSystemLoader, Environment, Template

env = Environment(
    loader=FileSystemLoader(
        "C:/Users/Adedara/OneDrive/Personal Work/kjbackend/app/templates"
        )
    )
template = env.get_template("WaitlistTemplate.html")

def render_template(**kwargs) -> str:
    """Render the template with the given context variables."""
    return template.render(**kwargs)


# if __name__ == "__main__":
#     # Example usage
#     context = {
#         "username": "Adedara",
#     }
    
#     rendered_html = render_template(**context)
#     print(rendered_html)