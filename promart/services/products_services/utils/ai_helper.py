# import openai
# import logging
# from django.conf import settings

# # Configure logging
# logger = logging.getLogger(__name__)

# # Set OpenAI API key from Django settings
# openai.api_key = settings.OPENAI_API_KEY

# def generate_product_description(name):
#     """
#     Generate a detailed and engaging product description using OpenAI's GPT model.

#     This function sends a prompt to the OpenAI GPT-3.5-turbo model to generate a creative 
#     product description that can be used in e-commerce platforms.

#     Args:
#         name (str): Name of the product.

#     Returns:
#         str: Generated product description or an error message if something goes wrong.
#     """
#     prompt = f"Write an engaging and detailed description for a product named {name}."
#     logger.info(f"Generating product description for: {name}")

#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a professional e-commerce product writer."},
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=200,
#             temperature=0.7
#         )
#         description = response["choices"][0]["message"]["content"].strip()
#         logger.info("Product description generated successfully.")
#         return description

#     except openai.OpenAIError as e:
#         logger.error(f"OpenAI API error: {e}")
#         return f"Error generating product description: {e}"

#     except Exception as e:
#         logger.exception(f"Unexpected error: {e}")
#         return f"An unexpected error occurred: {e}"
