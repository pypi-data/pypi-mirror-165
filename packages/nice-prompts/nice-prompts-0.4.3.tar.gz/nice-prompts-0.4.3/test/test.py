import nice_prompts

n = nice_prompts.NicePrompt()

print("Do you wish to take part in this short survey?", end=" ")

print(n.confirm())

print(n.number(float, 0, 1))

print(n.number(int, 0, 100))

print(n.number(int, 10))

print(
    n.selection(
        {
            "I like pizza": "Good taste",
            "I respectfully disagree with the opinion of liking pizza": "Fair enough, good day",
            "I hate pizza": "Bad sport 👎",
        }
    )
)  # Select one from the keys, return the value

print(
    n.multiselection(
        {
            "I like pizza": "Good taste",
            "I respectfully disagree with the opinion of liking pizza": "Fair enough, good day",
            "I hate pizza": "Bad sport 👎",
        },
        amount=2,
        required=2,
    )
)  # Select multiple from the keys, return the values. You must select 2


print(
    n.multiselection(
        {
            "I like pizza": "Good taste",
            "I respectfully disagree with the opinion of liking pizza": "Fair enough, good day",
            "I hate pizza": "Bad sport 👎",
        },
        required=0,
    )
)  # Select multiple from the keys, return the values. No max, can be left blank
