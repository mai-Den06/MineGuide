from modules.db_handler import insert_object, create_tables

def insert_initial_data():
    """ 初期データを挿入する """
    objects = [
        ("iron_ore", "地表や洞窟で採掘でき\nかまどで精錬すると鉄のインゴットが得られる"),
    ]

    for name, description in objects:
        insert_object(name, description)

if __name__ == "__main__":
    create_tables()
    insert_initial_data()
    print("Initial data inserted successfully.")
