from ai import call_gpt

def main():
    name = input("Enter your name: ")
    print(f"\nWelcome to the Movie Quiz, {name}!\n")

    num_questions = input("How many questions would you like? ")
    try:
        num_questions = int(num_questions)
    except ValueError:
        print("Invalid input, using 3 questions.")
        num_questions = 3

    print("\nGetting your quiz ready...")

    prompt = (f"Create a {num_questions}-question movie quiz with multiple choice (A-D). Format like:\n" \
             "1. Question text?\nA. Option A\nB. Option B\nC. Option C\nD. Option D\n\n" \
             "Answers:\n1. A\n2. C\n...")

    quiz_text = call_gpt(prompt)
    lines = quiz_text.strip().splitlines()

    questions = []
    answers = {}

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.lower().startswith("answers"):
            break
        if line and line[0].isdigit() and '.' in line:
            q = line
            opts = {}
            for j in range(1, 5):
                if i + j < len(lines):
                    opt_line = lines[i + j].strip()
                    if len(opt_line) > 2 and opt_line[1] == '.':
                        opts[opt_line[0]] = opt_line[3:]
            questions.append((q, opts))
            i += 4
        i += 1

    # Parse answers
    for line in lines:
        if line.strip().lower().startswith("answers"):
            continue
        if '.' in line:
            parts = line.strip().split('.')
            if len(parts) == 2:
                try:
                    qnum = int(parts[0].strip())
                    ans = parts[1].strip().upper()
                    if ans in ['A', 'B', 'C', 'D']:
                        answers[qnum] = ans
                except:
                    pass

    # Run quiz
    score = 0
    for idx, (question, opts) in enumerate(questions):
        print(f"\n{question}")
        for key in ['A', 'B', 'C', 'D']:
            print(f"  {key}. {opts.get(key, 'N/A')}")
        ans = input("Your answer (A/B/C/D): ").strip().upper()
        correct = answers.get(idx + 1)
        if ans == correct:
            print("✅ Correct!")
            score += 1
        else:
            print(f"❌ Wrong. The correct answer was {correct}.")

    print(f"\n🎉 Done! {name}, your score: {score}/{len(questions)}")

if __name__ == "__main__":
    main()
