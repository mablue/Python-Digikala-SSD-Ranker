import requests
import json
import re


def extract_size(name):
    name = name.replace('یک', '1')
    name = name.replace('دو', '2')
    name = name.replace('سه', '3')
    name = name.replace('چهار', '4')
    name = name.replace('پنج', '5')
    name = name.replace('شش', '6')
    name = name.replace('شیش', '6')
    name = name.replace('هفت', '7')
    name = name.replace('هشت', '8')
    name = name.replace('نه', '9')
    name = name.replace('ده', '10')
    name = name.replace('یازده', '11')
    """Extracts the size in gigabytes from a product name.

    Args:
        name (str): The product name.

    Returns:
        int: The size in gigabytes, or None if no size is found.
    """

    # Define patterns for common size expressions
    patterns = [
        r"\d+(\.\d+)?(?= گیگابایت)",  # Matches numbers followed by "گیگابایت"
        r"\d+(\.\d+)?(?= ترابایت)",  # Matches numbers followed by "ترابایت"
        r"\d+(\.\d+)?(?=GB)",       # Matches numbers followed by "GB"
        r"\d+(\.\d+)?(?=TB)",       # Matches numbers followed by "TB"
    ]

    for pattern in patterns:
        match = re.search(pattern, name)
        if match:

            size = float(match.group())

            if "ترابایت" in name or "TB" in name:
                size *= 1024  # Convert terabytes to gigabytes
            return size

    return None


def sort_by_rank(data):
  """Sorts a list of SSD products by their rank in descending order.

  Args:
    data: A list of dictionaries, where each dictionary represents an SSD product.

  Returns:
    A new list of sorted dictionaries.
  """

  return sorted(data, key=lambda x: x['rank'], reverse=True)


ssd_data = []


for page_num in range(1,10):
    url = f"https://api.digikala.com/v1/categories/internal-sdd/search/?page={page_num}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-200 status codes
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching data: {e}")
        exit(1)

    # Parse the JSON data
    try:
        data = json.loads(response.text)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON data: {e}")
        exit(1)


    # Extract names and prices
    products = data.get("data", {}).get("products", [])  # Handle potential missing keys
    for product in products:
        
        name = product.get("title_fa")
        price = product.get("default_variant", {}).get("price", {}).get("selling_price")
        size = extract_size(name)

        # Check if name and price exist before printing
        if name and price and size:
            print(f"Name: {name}")
            print(f"Price: {price}")
            rank = size/price*10000
            print(f"Size: {size} GB")
            print(f"Rank: {rank:.3f}\n")
            ssd_data.append({
                'name' : name,
                'price' : price,
                'size' : size,
                'rank' : rank,
            })
        elif not name:
            print(f"Name not found\n")
        elif not price:
            print(f"Price not found for: {name}\n")
        elif not size:
            print(f"Size not found for: {name}\n")



# Assuming your data is stored in a list named 'ssd_data'
sorted_ssd_data = sort_by_rank(ssd_data)

# Print the sorted data
for ssd in sorted_ssd_data:
  print(ssd)
