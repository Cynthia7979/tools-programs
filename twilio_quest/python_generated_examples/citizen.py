class Citizen:
  """Describes the class"""
  greeting = "For the glory of Python!"
  def __init__(self, first_name, last_name):
    self.first_name, self.last_name = first_name, last_name
  def full_name(self): return f"{self.first_name} {self.last_name}"
