In this test, you are creating a simple web app with two actors (users), the "end user" and a "reviewer". The objective of the app is to verify a working email address and mobile number.

1. Enrolment Request Web Form:
  - Capture name, company name, email, SMS#, phone number with extension
  - Check box for terms (lorem ipsum1)
  - CAPTCHA
  - Validate input and present to user any errors
2. Server action on Enrolment Request submission:
  - If email address or SMS# exists in redis or database, decline enrolment request — message to say "Error: account exists or is in the process of review."
  - else advise that request will be reviewed and responded to within 3 business days; mark request as review-pending
3. Batch process to be run by reviewer:
  - List a collection of pending requests (paginated)
  - A pending request should show the user details plus a unique generated URL:=hash(secret+email+SMS)
  - A pending request may be approved or rejected, with the result to be sent to the end user by email
  - All URLs and all review-pending accounts must expire after 5 days
4. Account Creation Request Webform at unique URL:
  - Lookup unique URL and check validity
  - Via XHR, validate the mobile phone number with OTP via SMS
  - User should nominate a password and agree to terms again
  - The user cannot proceed until the mobile phone number is validated
  - Limit OTP validation to 3 attempts, each attempt allows up to 60 seconds
  - A failed OTP validation cancels the enrolment process and the URL is invalidated
5. On validation success
  - Move and store credentials
  - Change account status to activation1 and present a welcome message to the end user

---

### Notes:

- A sandbox machine will be provided for the purpose of this test
- There will be a time constraint on the test; please advise when you are ready to start
- Document your work (configuration, usage, implementation notes [tech stack, DB/object schema, etc], decision choices/rationale)
- For sending SMS, build a pseudo-SMS service that accepts a mobile number and message as an input which always return 200 OK when both fields are not empty
