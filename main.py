import os
import time
import google.generativeai as genai # type: ignore

genai.configure(api_key=["AIzaSyDckDBylE6eYBEjaKpsqA_KWF5BgcXvUV8"])

def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

def wait_for_files_active(files):
  """Waits for the given files to be active.

  Some files uploaded to the Gemini API need to be processed before they can be
  used as prompt inputs. The status can be seen by querying the file's "state"
  field.

  This implementation uses a simple blocking polling loop. Production code
  should probably employ a more sophisticated approach.
  """
  print("Waiting for file processing...")
  for name in (file.name for file in files):
    file = genai.get_file(name)
    while file.state.name == "PROCESSING":
      print(".", end="", flush=True)
      time.sleep(10)
      file = genai.get_file(name)
    if file.state.name != "ACTIVE":
      raise Exception(f"File {file.name} failed to process")
  print("...all files ready")
  print()

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
)

# TODO Make these files available on the local file system
# You may need to update the file paths
files = [
  upload_to_gemini("jemh1a1.pdf", mime_type="application/pdf"),
]

# Some files have a processing delay. Wait for them to be ready.
wait_for_files_active(files)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        files[0],
        "Read this chapter thoroughly and create 20 MCQs for this chapter. Each question should have 4 options and 1 option should be correct.",
      ],
    },
    {
      "role": "model",
      "parts": [
        "**1. Which of the following is NOT a mathematical statement?**\n(a) The sum of two even numbers is even.\n(b) Close the door.\n(c) Every prime number greater than 2 is odd.\n(d) The square root of 2 is irrational.\n\n**2.  What is a statement that is neither always true nor always false called?**\n(a) Contradiction\n(b) Ambiguous\n(c) Converse\n(d) Negation\n\n**3. What is the core of constructing mathematical proofs?**\n(a) Inductive reasoning\n(b) Abductive reasoning\n(c) Deductive reasoning\n(d) Intuitive reasoning\n\n**4. What is the negation of \"All birds can fly\"?**\n(a) No birds can fly.\n(b) Some birds can fly.\n(c) Some birds cannot fly.\n(d) All birds cannot fly.\n\n**5. What is the converse of \"If it rains, then the ground is wet\"?**\n(a) If the ground is wet, then it rains.\n(b) If it does not rain, then the ground is not wet.\n(c) If the ground is not wet, then it does not rain.\n(d) It rains and the ground is wet.\n\n**6.  Which reasoning process is used to disprove a statement by providing a single example where it fails?**\n(a) Proof by contradiction\n(b) Counterexample\n(c) Converse\n(d) Deductive reasoning\n\n**7. Which term describes a meaningful sentence that is not a command, exclamation, or question?**\n(a) Premise\n(b) Statement\n(c) Hypothesis\n(d) Conclusion\n\n**8. What is an educated guess in mathematics called?**\n(a) Theorem\n(b) Axiom\n(c) Conjecture\n(d) Proof\n\n**9. What is the main tool used in constructing a proof?**\n(a) Conjecture\n(b) Negation\n(c) Deductive Reasoning\n(d) Converse\n\n**10. If p is a prime number greater than 3, which form can it NOT take?**\n(a) 6k + 1\n(b) 6k + 5\n(c) 6k + 3\n(d) None of the above\n\n**11. The negation of \"Some dogs are brown\" is:**\n(a) Some dogs are not brown.\n(b) All dogs are brown.\n(c) No dogs are brown.\n(d) Not all dogs are brown.\n\n**12. Which proof method involves assuming the opposite of what you want to prove and arriving at a contradiction?**\n(a) Direct proof\n(b) Proof by exhaustion\n(c) Proof by contradiction\n(d) Proof by induction\n\n**13.  What is a series of logical deductions from premises leading to a conclusion called?**\n(a) Hypothesis\n(b) Proof\n(c) Conjecture\n(d) Negation\n\n**14. What is the negation of \"There is no integer x such that x² = -1\"?**\n(a) There is an integer x such that x² = -1\n(b) There is no integer x such that x² = 1\n(c) For all integers x, x² ≠ -1\n(d) For some integer x, x² = -1\n\n**15. The sum of two rational numbers is always a:**\n(a) Irrational Number\n(b) Rational Number\n(c) Integer\n(d) Whole Number\n\n**16. Which of the following is an example of an ambiguous statement?**\n(a) The sky is blue.\n(b) Cars have four wheels.\n(c) 2 + 2 = 4\n(d) All prime numbers are odd.\n\n**17. Which of the following describes the relationship between a statement and its converse?**\n(a) They are always both true or both false.\n(b) If the statement is true, the converse must be false.\n(c) The converse is formed by switching the hypothesis and conclusion.\n(d) The converse is the negation of the statement.\n\n\n**18.  If a statement is represented by 'p', how is its negation represented?**\n(a) -p\n(b) /p\n(c) ~p\n(d) q\n\n**19. A statement and its negation have:**\n(a) Opposite truth values\n(b) The same truth value\n(c) Sometimes the same, sometimes different truth values\n(d) No relation to each other.\n\n**20. What is a statement that has been proven true called?**\n(a) Hypothesis\n(b) Conjecture\n(c) Theorem\n(d) Axiom",
      ],
    },
  ]
)

response = chat_session.send_message("INSERT_INPUT_HERE")

print(response.text)