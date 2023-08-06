from jinja2 import Environment, FileSystemLoader

def generate_file():
  file_loader = FileSystemLoader('src/huble/sklearn/templates')
  env = Environment(loader=file_loader)
  template = env.get_template('script.j2')
  output = template.render(name='Rugved')
  print(output)