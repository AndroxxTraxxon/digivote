import sqlite3
import os

class DAOError(IOError):
  pass

class DAOConnectionError(DAOError):
  pass

class DAO(object):
  
  tables = dict()
  settingsTableName = "_settings"
  version = "0.0.1"
  settings = {
    "version": version
  }

  def __init__(self, filepath:str = None):
    self.filepath = filepath


  def __enter__(self):
    if self.init_conn():
      self.init_settings()
    else:
      raise DAOConnectionError("Unable to open Database Connection")
    return self

  def __exit__(self, _, __, ___):
    # print(_, __, ___)
    self.cursor.close()
    self.conn.close()


  def init_conn(self):
    if self.filepath is None:
      self.filepath = os.path.join(os.getcwd(), "tmp.db")
    print("Opening DB at {}".format(self.filepath))
    try:
      self.conn = sqlite3.connect(self.filepath)
      self.cursor = self.conn.cursor()
      return True
    except OSError as e:
      print(e)

    return False

  def init_settings(self):
    if(self.settings_exist()):
      self.read_settings()
    else:
      # create settings table
      self.create_table(self.settingsTableName, [
        ("_name", "text", "PRIMARY KEY"),
        ("_value", "text", "NOT NULL")
      ])
      # write basic settings into the db.
      self.generate_settings()
  
      pass
  
  def generate_settings(self):
    import secrets
    print("Generating settings!")
    self.settings["key"] = secrets.token_hex(64)
    self.save_settings()
    
  
  def save_settings(self):
    insertItems = [(key, value) for key, value in self.settings.items()]
    print("Saving settings!")
    self.conn.executemany("""
    INSERT INTO {} ('_name', '_value')
    VALUES (?, ?)
    """.format(self.settingsTableName), insertItems)
    self.conn.commit()
  
  def read_settings(self):
    result = self.conn.execute("""
    SELECT _name as [name], _value as [value] FROM {}
    """.format(self.settingsTableName))
    for row in result:
      if(row[0] == "version" and 
         not row[1] == self.settings["version"]):
         DAOError("Mismatched DB version!")
      else:
        self.settings[row[0]] = row[1]

  def create_table(self, table_name, columns, constraints = None):
    columns = ",\n  ".join (["{name} {type}{constraint}".format(
      name= column[0],
      type= column[1],
      constraint = "" if (len(column) <= 2 or column[2] is None) else (" " + column[2])
    ) for column in columns])

    det = columns

    if constraints is not None:
      constraints = ",\n  ".join(constraints)
      det = ",\n  ".join([columns, constraints])

    sql_txt = "CREATE TABLE IF NOT EXISTS {name} (\n  {details}\n)".format(
      name=table_name,
      details=det
      )
    self.conn.execute(sql_txt)

  def settings_exist(self):
    sql_text = """
      SELECT 1 FROM sqlite_master WHERE
      type = 'table' AND name = '{table_name}'
    """.format(table_name = self.settingsTableName)
    result = self.conn.execute(sql_text)
    for row in result:
      return True
    # if the result is empty, we won't have returned true
    return False



if __name__ == "__main__":
  filepath = os.path.join(os.getcwd(), "temp_data.db")
  with DAO(filepath) as db:
    print(DAO.settings)

