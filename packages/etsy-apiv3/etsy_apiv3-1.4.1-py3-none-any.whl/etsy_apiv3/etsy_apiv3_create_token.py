from requests_oauthlib import OAuth2Session


from requests_oauthlib import OAuth2Session

CLIENT_KEY = "hdvqwd0po24bcbnpb3p8m7c9"
CLIENT_SECRET = "ja6xhs76se"

auth = OAuth2Session(redirect_uri="https://www.upscontrol.com", scope=["transactions_r", "transactions_w", "shops_w", "shops_r", "recommend_w", "recommend_r", "profile_w", "profile_r", "listings_w", "listings_r", "listings_d", "feedback_r", "favorites_r", "favorites_w", "email_r", "cart_w", "cart_r", "address_w", "address_r", "billing_r"], client_id=CLIENT_KEY)

authorization_url, state = auth.authorization_url("https://www.etsy.com/oauth/connect", state="superstate", code_challenge="QphiomoJBpNalZrZuEyX1yrhPaSNu7SHhcHUO_i6QMI", code_challenge_method="S256")

print(authorization_url)

#auth_response = input("Auth Response: ")
code = input("Code: ")
token = auth.fetch_token(
    token_url="https://api.etsy.com/v3/public/oauth/token",
    code=code,
    state="superstate",
    client_id=CLIENT_KEY,
    code_verifier="2jsEWXie7aLMm7dlirVCBo3VGcFOUvujZChTAoo3ZsSe5CStqC_RHitWoHkeo5HFfWt3EG5Aqod-pfstHc4PUig1aSGb-hksdlUuy-4oiM1_Vb1rX0fSewHVNidCFwDt",
    include_client_id=True
)
print(token)