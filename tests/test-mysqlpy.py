from mysqlpy import MySQLPy


s = MySQLPy(host='localhost', user='root', pwd='')
s.select_db('ict_discovery')

for i in (s.select_all('wp_options')):
    print(i)

# print(s.get_all_dbs())
# s.db_exists('performanc_schema')
# s.create_db("Sahan")
# s.delete_db("Sahan")
# print(s.get_all_tbs())
# print(s.tb_exists('wp_comments'))
# s.create_tb()

# s.add_record('countries', ["Iraq", "Kabul", "Arabic", "90%"])
# s.get_tb_cols('countries')
# print(s.select_all('countries', {}))
# print(s.select_all('countries', {"Name": 'ASC'}))
# print(s.select_all('countries', {"Name": 'DESC'}))
# print(s.select_all('countries', {"": 'DESC'}))
# print(s.select_filtered('countries', ["name", "capital"]))
# print(s.select_filtered('countries', ['Name', 'capital'], 'capital="Rio"'))
# s.delete_record('countries', 'Name="Hungaria"')
# s.update_tb('friends', 'name', 'Mark', '')
# s.update_tb('friends', 'name', 'Smoky Fuck', 'telephone=11')
# s.create_tb('friends', {'Name': 'varchar(255)', "Age": "int(100)"}, 'name')
# print(s.select_all('friends'))
# print(s.explain_tb('friends'))
# s.add_record('friends', ['Sahan', 25])
