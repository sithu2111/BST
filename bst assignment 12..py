"""This program includes using Binary Search Tree with complete CRUD operations.
 The mysql database is used to store previous data.
Created by Sithunyunt (DIP-2)
submitted on 9/7/2023..."""


import random
import mysql.connector


class Node:
    def __init__(self, ID, name, email, password, phone):
        self.ID = ID
        self.name = name 
        self.email = email
        self.password = password
        self.phone = phone
        self.left = None
        self.right = None


class User_profile:
    def __init__(self):
        self.root = None
        self.fetch()
        self.delete_insql()
        

    def root_node(self, ID, name, email, password, phone):
        new_node = Node(ID, name, email, password, phone)
        if self.root is None:
            self.root = new_node
        else:
            self.insert_node(self.root, new_node)


    def insert_node(self, current_node: Node, new_node: Node):
        if new_node.ID < current_node.ID:
            if current_node.left is None:
                current_node.left = new_node
            else:
                self.insert_node(current_node.left, new_node)
        elif new_node.ID > current_node.ID:
            if current_node.right is None:
                current_node.right = new_node
            else:
                self.insert_node(current_node.right, new_node)
        else:
            pass


    def save_in_mysql(self, user_list):
        mydb = mysql.connector.connect(
        host = "localhost",
        user = "Sithu",
        password = "sithu2111",
        database = "Dip2")
        cursor = mydb.cursor()
        insert_query = "INSERT INTO users (ID, name, email, password, phone) VALUES (%s, %s, %s, %s, %s)"
        for user in user_list:
            cursor.execute(insert_query, user)
        mydb.commit()
        cursor.close()
        mydb.close()


    def fetch(self):
        mydb = mysql.connector.connect(
        host = "localhost",
        user = "Sithu",
        password = "sithu2111",
        database = "Dip2")
        cursor = mydb.cursor()
        select_query = "SELECT * FROM users"
        cursor.execute(select_query)
        user_records = cursor.fetchall()
        for user in user_records:
            self.root_node(user[0], user[1], user[2], user[3], user[4])
        cursor.close()
        mydb.close()


    def delete_insql(self):
        mydb = mysql.connector.connect(
        host = "localhost",
        user = "Sithu",
        password = "sithu2111",
        database = "Dip2")
        cursor = mydb.cursor()
        cursor.execute("DELETE FROM users")
        mydb.commit()
        cursor.close()
        mydb.close()


    def save_data(self, node: Node):
        nodes = []
        if node:
            self.save_data(node.left)
            nodes.append((node.ID, node.name, node.email, node.password, node.phone))
            self.save_data(node.right)
        self.save_in_mysql(nodes)


    def input_checking(self):
        try:
            user_input = int(input("\nPress 1 to create a new account:\nPress 2 to log in to your account:\nPress 3 to Exit: "))
            if user_input == 1:
                self.register()

            elif user_input == 2:
                self.login()

            elif user_input == 3:
                print("Exit loading-----")
                self.save_data(self.root)
                self.inordertraversal(self.root)
                exit(1)

            else:
                print("Choose between '1', '2' or '3'")

        except Exception as err:
            print(err)
            

    def register(self):
        print("Please fill in the following form to create a new account.")

        try:
            user_name = input("Enter your name to register: ").title()
            user_id = random.randint(1, 500)
            while True:
                user_email = input("Enter your email to register: ")
                if self.form_check(user_email) == -1:
                    print("Email form invalid!\n Please Try again!")
                else:
                    break   
            if self.email_check(user_email, self.root):
                print("Email was already registered!\n You can login now.")
                self.input_checking()
            else:   
                user_password = input("Create your password to register: ")
                while True:
                    user_phone = input("Enter your phone number: 09")
                    if self.phone_validation(user_phone)[0] == -1:
                        print("Phone number invalid!\nPlease Try again!")
                    else:
                        break
                u_phone = self.phone_validation(user_phone)[1]
                if self.phone_check(u_phone, self.root):
                    print("Your phone is already registered!\n You can login now.")
                    self.input_checking()
                self.root_node(user_id, user_name, user_email, user_password, u_phone)
                print("Your ID number is: ", user_id)
                print("Regristration Successful!")
                       
        except Exception as err:
            print(err)
        

    def form_check(self, u_email):
        name_count = 0
        for i in range(len(u_email)):
            if u_email[i] == "@":
                break
            name_count += 1

        email_name = u_email[0: name_count]
        email_form = u_email[name_count:]

        email_flag = 0
        name_flag = 0

        for i in range(len(email_name)):
            aChar = email_name[i]
            if (31 < ord(aChar) < 48) or (57 < ord(aChar) < 65) or (90 < ord(aChar) < 97) or (122 < ord(aChar) < 128):
                name_flag = -1
                break

        domain_form = ["@facebook.com", "@apple.com", "@zoho.com", "@gmail.com", "@yahoo.com", "@mail.ru"]
        for i in range(len(domain_form)):
            if domain_form[i] == email_form:
                email_flag = -1
                break

        if name_flag == 0 and email_flag == -1:
            return 1
        else:
            return -1

                
    def email_check(self, u_email, node: Node):
        if node:
            if node.email == u_email:
                return True
            if self.email_check(u_email, node.left):
                return True
            if self.email_check(u_email, node.right):
                return True
       

    def phone_validation(self, u_phone):
        fixed_prefix = "09"
        if len(u_phone) == 9 and u_phone.isdigit():
            phone_number = fixed_prefix + u_phone
            return (1, phone_number)
        else:
            return -1,

    
    def phone_check(self, u_phone, node: Node):
        if node:
            if node.phone == u_phone:
                return True
            if self.phone_check(u_phone, node.left):
                return True
            if self.phone_check(u_phone, node.right):
                return True
            

    def login(self):
        print("\nThis is login section...\nYou can log in by using either your email address or your phone number.")
        user_input = int(input("Press 1 to log in by your email:\nPress 2 to log in by your phone: "))
        if user_input == 1:
            self.l_check_by_email()
        elif user_input == 2:
            self.l_check_by_phone()
        else:
            print("Please choose '1' or '2' ")

        
    def l_check_by_email(self):
        while True:
                l_email = input("Enter your email to log in to your account: ")
                if self.form_check(l_email) == -1:
                    print("Email form invalid!\n Please Try again!")
                else:
                    break   
        login_result = self.login_check_by_mail(l_email, self.root)
        if login_result[0] == 1:
            user = login_result[1]
            print("\nWelcome, ", user.name)
            print("Your ID number: ", user.ID)
            print("Your password: ", user.password)
            print("Your Phone Number: ", user.phone)
            self.user_choice(user)
        else:
            print("Login failed!")
            self.input_checking()

    def login_check_by_mail(self, email, node: Node):
        if node is None:
            return 0, None

        if node.email == email:
            return 1, node

        left_flag, left_node = self.login_check_by_mail(email, node.left)
        if left_flag == 1:
            return 1, left_node

        right_flag, right_node = self.login_check_by_mail(email, node.right)
        if right_flag == 1:
            return 1, right_node

        return 0, None
            
    def l_check_by_phone(self):
        while True:
                    user_phone = input("Enter your phone number to log in to your account: 09")
                    if self.phone_validation(user_phone)[0] == -1:
                        print("Phone number invalid!\nPlease Try again!")
                    else:
                        break
        l_phone = self.phone_validation(user_phone)[1]
        login_result = self.login_check_by_phone(l_phone, self.root)
        if login_result[0] == 1:
            user: Node = login_result[1]
            print("\nWelcome, ", user.name)
            print("Your ID number: ", user.ID)
            print("Your password: ", user.password)
            print("Your Phone Number: ", user.phone)
            self.user_choice(user)
        else:
            print("Login failed!")
            self.input_checking()

    
    def login_check_by_phone(self, phone, node: Node):
        if node is None:
            return 0, None

        if node.phone == phone:
            return 1, node

        left_flag, left_node = self.login_check_by_phone(phone, node.left)
        if left_flag == 1:
            return 1, left_node

        right_flag, right_node = self.login_check_by_phone(phone, node.right)
        if right_flag == 1:
            return 1, right_node

        return 0, None
    

    def user_choice(self, user: Node):
        user_input = int(input("Press 1 to update your information:\nPress 2 to delete your account:\nPress 3 to go back to main menu: "))
        if user_input == 1:
            new_info = self.update(user)
            self.to_update(new_info, self.root)
            print("Your account has been successfully updated!\nYou can check by login.")

        elif user_input == 2:
            answer = input("Are you sure you want to delete your account? Y or N: ")
            if answer == "Y":
                self.delete(user, self.root)
                print("Your account has been successfullly deleted.")
            else:
                self.input_checking()
            
        elif user_input == 3:
            self.input_checking()

        else:
            print("Numbers only!!")
            self.user_choice(user)
           

    def update(self, user: Node):
        user_input = int(input("\n*1 to update Name: \n*2 to update Email:\n*3 to update Password:\n*4 to update Phone: "))
        if user_input == 1:
            new_name = input("Enter your new name: ").title()
            user.name = new_name
            return user
            
        elif user_input == 2:
            while True:
                new_email = input("Enter your new email: ")
                if self.form_check(new_email) == -1:
                    print("Email form invalid!\n Please Try again!")
                else:
                    break   
            user.email = new_email
            return user

        elif user_input == 3:
            new_password = input("Enter your password: ")
            user.password = new_password
            return user
        
        elif user_input == 4:
            while True:
                    new_phone = input("Enter your new phone number: 09")
                    if self.phone_validation(new_phone)[0] == -1:
                        print("Phone number invalid!\nPlease Try again!")
                    else:
                        break
            n_phone = self.phone_validation(new_phone)[1]
            user.phone = n_phone
            return user
        

    def to_update(self, update_node:Node, node: Node):
        if node:
            if node.ID == update_node.ID:
                node = update_node
                return node
            
            if self.to_update(update_node, node.left):
                left_node = self.to_update(update_node, node.left)
                return left_node
            
            if self.to_update(update_node, node.right):
                right_node = self.to_update(update_node, node.right)
                return right_node


    def delete(self, user_node: Node, root: Node):
        if root is None:
            return root       
        if root.ID > user_node.ID:
            root.left = self.delete(user_node, root.left)
        elif root.ID < user_node.ID:
            root.right = self.delete(user_node, root.right)
        else:
            if root.left is None:
                temp = root.right
                del root
                return temp
            elif root.right is None:
                temp = root.left
                del root
                return temp
            else:
                root = self.minValuenode(root.right)
                root.right = self.delete(root, root.right)

        return root


    def minValuenode(self, node: Node):
        current = node
        while current.left is not None:
            current = current.left
        return current
            
       
    def inordertraversal(self, node):
        if node:
            self.inordertraversal(node.left)
            print("ID", node.ID)
            self.inordertraversal(node.right)


if __name__ == "__main__":
    user = User_profile()
    while True:
        user.input_checking()
    
            
    