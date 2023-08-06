from .helloworld import HelloWorld 

def my_first_entry_point_funtion():
    print("Look ma, I'm an entry point!")

def my_second_entry_point_funtion():
    helloworld=HelloWorld()
    helloworld.print_message()