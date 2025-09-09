# Give me a program to convert fahrenheit to celcius

def fahrenheit_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius using the formula: C = (F - 32) * 5/9"""
    celsius = (fahrenheit - 32) * 5/9
    return celsius

def main():
    try:
        # Get input from user
        temp_f = float(input("Enter temperature in Fahrenheit: "))
        
        # Convert to Celsius
        temp_c = fahrenheit_to_celsius(temp_f)
        
        # Display result
        print(f"{temp_f}°F = {temp_c:.2f}°C")
        
    except ValueError:
        print("Please enter a valid number.")

if __name__ == "__main__":
    main()

