"""
Pool of 100 unique Indian names used to populate buyers, sellers, and
delivery drivers for a simulation run.
"""

NAME_POOL = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan",
    "Krishna", "Ishaan", "Rohan", "Kabir", "Aryan", "Dhruv", "Karthik", "Manav",
    "Nikhil", "Rahul", "Rajesh", "Sanjay", "Amit", "Vikram", "Suresh", "Ramesh",
    "Anil", "Deepak", "Gaurav", "Harsh", "Varun", "Yash", "Siddharth", "Tarun",
    "Uday", "Vikas", "Abhishek", "Ashwin", "Chirag", "Devendra", "Girish", "Hemant",
    "Jatin", "Kunal", "Lakshay", "Mohit", "Naveen", "Omkar", "Pranav", "Rajat",
    "Saurabh", "Tanmay", "Aanya", "Diya", "Ira", "Kiara", "Myra", "Pari",
    "Riya", "Saanvi", "Sara", "Zara", "Ananya", "Bhavya", "Chitra", "Divya",
    "Esha", "Falguni", "Gauri", "Hema", "Isha", "Jaya", "Kavya", "Lakshmi",
    "Meera", "Nandini", "Ojasvi", "Pooja", "Radhika", "Sneha", "Tanvi", "Uma",
    "Vidya", "Yamini", "Anjali", "Bela", "Charu", "Deepika", "Ekta", "Farah",
    "Geeta", "Hina", "Indira", "Janvi", "Kiran", "Leela", "Madhavi", "Neha",
    "Pallavi", "Priya", "Ritika", "Simran",
]

assert len(NAME_POOL) == len(set(NAME_POOL)) == 100, "Name pool must have exactly 100 unique names"
