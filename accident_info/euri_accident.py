from euriai import EuriaiClient



location="delhi"

prompt=f"""
    As a professional news reporter, provide:  
1. A 50-60 word verified road accident update for {location} (15 km radius). If none, state 'No recent updates found on {location} or nearby.'  
2. The fastest route from Bhauti to {location}, listing exact roads/highways.  
Avoid explanations, links (if no news), and internal thinking. Be concise.

Mention the exact roads/highways to be taken.
"""                    

client = EuriaiClient(
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiIxZWU2NTg0MS1hZDQ0LTQ1YmMtODcxNy1kZDRkNzM2ZTE1YjIiLCJlbWFpbCI6ImFsb2t0cmlwYXRoaTA3MEBnbWFpbC5jb20iLCJpYXQiOjE3NDYwNjM1NDQsImV4cCI6MTc3NzU5OTU0NH0.r17aL4xvJnvhrfGJzalSTjerrh6RG09kkGKd6qe7Rd4",
    model="llama-4-scout-17b-16e-instruct"
)

response = client.generate_completion(
    prompt=prompt,
    temperature=0.7,
    max_tokens=500
)

response = response['choices'][0]['message']['content']
print(response)
