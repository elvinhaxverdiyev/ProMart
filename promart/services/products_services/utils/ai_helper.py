# import openai
# from django.conf import settings

# # OpenAI API açarını settings-dən əldə edirik
# openai.api_key = settings.OPENAI_API_KEY

# def generate_product_description(name):
#     """
#     Generates an engaging and detailed product description using OpenAI's GPT model.

#     This function takes a product name as input and uses OpenAI's GPT-3.5 model to generate
#     a creative and detailed description for the product. The generated description can be
#     used in an e-commerce platform to enhance the product's appeal.

#     Args:
#         name (str): The name of the product for which the description is to be generated.

#     Returns:
#         str: The generated product description.
#     """
#     prompt = f"Write an engaging and detailed description for a product named {name}."

#     try:
#         # Create a ChatCompletion request with OpenAI API
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",  # Yeni model adı
#             messages=[  # Yeni interfeys formatında mesajlar göndərilir
#                 {"role": "system", "content": "You are a professional e-commerce product writer."},
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=200,
#             temperature=0.7
#         )
        
#         # Return the generated product description
#         return response['choices'][0]['message']['content'].strip()
    
#     except openai.OpenAIError as e:
#         # Handle API errors (e.g., connection issues, quota limits)
#         return f"Error generating product description: {e}"

#     except Exception as e:
#         # General error handler
#         return f"An unexpected error occurred: {e}"
