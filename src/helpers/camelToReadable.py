def camelToReadable(camelCaseName):
  readableName = "".join([" " + char if char.isupper() else char for char in camelCaseName]).strip()
  return readableName.title()
