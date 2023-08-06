from blessed import Terminal
import sys
import string
import time


class NicePrompt:
    """Make nice prompts to gather input from the user e.g. multiple choice

    Args:
        terminal (blessed.Terminal): Supply a blessed terminal to use. Defaults to a new blessed terminal

    """

    def __init__(self, terminal=Terminal()):
        self.terminal = terminal

    def selection(self, options):
        """Choose an item from a dictionary of options. Keys are availiable
        options, values are what the function will return if that option is selected

        Args:
            options (dict): A dictionary of options. Keys are availiable
                options, values are what the function will return if that option
                is selected

        Returns:
            Object: The value from the options dictionary that the user selected
        """
        _ = self.terminal

        selected = 0

        # Print out all the options, selected option has an arrow

        for c, i in enumerate(options.keys()):
            if c == selected:
                filler = " " * (_.width - (len(i) + 5))
                print(f"{_.lightgreen} > {_.normal}{i}{filler}")
            else:
                filler = " " * (_.width - (len(i) + 5))
                print(f" ◦ {i}{filler}")

        with _.cbreak(), _.hidden_cursor():
            while True:
                val = _.inkey()
                if (
                    val.code == 343 or val.lower() == " "
                ):  # If enter or space is pressed
                    break
                if val.code == 258:  # Down arrow
                    selected += 1
                    # If selected goes higher than the list of options
                    if selected > len(options) - 1:
                        selected = 0  # Wrap it around to zero
                if val.code == 259:  # Up arrow
                    selected -= 1
                    if (
                        selected < 0
                    ):  # Much the same as above, just the other way around
                        selected = len(options) - 1

                # Move up to the top of the options list, so we can print it again
                p = _.move_up(len(options))
                print(p, end="")
                sys.stdout.flush()

                # Print out all the options, selected option has an arrow
                for c, i in enumerate(options.keys()):
                    if c == selected:
                        filler = " " * (_.width - (len(i) + 5))
                        print(f"{_.lightgreen} > {_.normal}{i}{filler}")
                    else:
                        filler = " " * (_.width - (len(i) + 5))
                        print(f" ◦ {i}{filler}")

        for i in range(len(options) + 1):  # Clear the options list to tidy up terminal
            print(f"{_.move_up}{_.clear_eol}{_.move_up}")

        # Print out the selected option
        print(f"{_.lightgreen}{list(options.keys())[selected]}{_.normal}")

        return options[list(options.keys())[selected]]

    def multiselection(self, options, amount=-1, required=1):
        """Choose some items from a dictionary of options. Keys are availiable
        options, values are what the function will return if that option is selected

        Args:
            options (dict): A dictionary of options. Keys are availiable
                options, values are what the function will return if that option
                is selected

            amount (int, optional): The max amount of items the user can
                select. Leave out for no limit.

            required (int, optional): The minimum amount of items the user can select. Defaults to 1.

        Returns:
            list[Object]: A list of the values from the options dictionary that the user selected
        """

        # This is very much similar to the above function, so a lot of it is not commented

        if amount == -1:
            amount = len(options)

        _ = self.terminal

        selected = 0

        chosen = []
        p = ""

        def print_list():
            nonlocal p
            print(p, end="")
            sys.stdout.flush()
            maxstr = f"Max {amount}." if amount < len(options) else ""
            if len(chosen) >= required:
                outof = f"/{required} required" if required > 0 else ""
                a = f"{_.lightgreen}{len(chosen)}{_.normal}{outof}. {maxstr}"
            else:
                a = f"{_.red}{len(chosen)}{_.normal}/{required} required. {maxstr}"
            print(f"Press space to choose an option, enter to finish. Selected {a}")
            for c, i in enumerate(options.keys()):
                if c == selected and c in chosen:
                    filler = " " * (_.width - (len(i) + 5))
                    print(f"{_.lightgreen} 🭬 {i}{_.normal}{filler}")
                elif c == selected:
                    filler = " " * (_.width - (len(i) + 5))
                    print(f"{_.lightgreen} 🭬 {_.normal}{i}{filler}")
                elif c in chosen:
                    filler = " " * (_.width - (len(i) + 5))
                    print(f"{_.lightgreen} • {i}{_.normal}{filler}")
                else:
                    filler = " " * (_.width - (len(i) + 5))
                    print(f" ◦ {i}{filler}")

            p = _.move_up(len(options) + 1)

        print_list()
        with _.cbreak(), _.hidden_cursor():
            while True:
                val = _.inkey()
                if val.code == 343 and len(chosen) >= required:
                    break
                if val.lower() == " ":
                    # If the selcted item is not chosen and the maximum amount of items has not been reached, choose this item
                    if not (selected in chosen) and len(chosen) != amount:
                        chosen.append(selected)
                    elif selected in chosen:  # If it is chosen, unchoose it
                        chosen.remove(selected)
                if val.code == 258:
                    selected += 1
                    if selected > len(options) - 1:
                        selected = 0
                if val.code == 259:
                    selected -= 1
                    if selected < 0:
                        selected = len(options) - 1

                print_list()

        for i in range(len(options) + 1):
            print(f"{_.move_up}{_.clear_eol}{_.move_up}")

        if (
            chosen
        ):  # List with values is true-ish, so this will be true if there are chosen items
            print(
                ", ".join(
                    [
                        f"{_.lightgreen}{i}{_.normal}"
                        for i in [list(options.keys())[i] for i in chosen]
                    ]
                )
            )  # print a list of selected items if there are any chosen
        else:
            # if no items were chosen, print that
            print(f"{_.red}No options selected{_.normal}")

        return [options[list(options.keys())[i]] for i in chosen]

    def number(self, number_type, start=None, end=None, check=lambda x: True):
        """The user can enter a number with optional bounds

        Args:
            number_type (class): The class of the number you want the user to enter. e.g. int float
            start (int, optional): The minimum number the user can enter. Leave out for no minimum
            end (int, optional): The maximum number the user can enter. Leave out for no maximum
            check (function, optional): A function that will be passed the number. Should return true or false, which will
                be used to check if the entered number is valid. You can use this for extra checks e.g. prime numbers
        Returns:
            type(number_type): The number the user entered
        """
        _ = self.terminal

        with _.cbreak():
            fromstr = ""
            if start != None or end != None:  # if bounds were specified
                if start != None and end != None:
                    fromstr = f" from {start} to {end}"
                elif start != None:
                    fromstr = f" starting from {start}"
                else:
                    fromstr = f" up to {end}"
            # make a prompt
            prompt = f"Please enter a {_.bright_yellow}{str(number_type.__name__)}{_.normal}{fromstr}."
            print(prompt)
            num = ""  # the string
            csr = 0  # cursor position
            # whether the number entered is valid (within bounds and of the specified type)
            valid = False
            while True:
                val = _.inkey()
                if val.code == 330 or val.code == 263:  # backspace or delete
                    if len(num) > 0:  # if there are characters in the input
                        # remove character at cursor from string
                        num = num[: csr - 1] + num[csr:]
                        csr -= 1  # move cursor back
                elif (
                    val.code == 260 and csr > 0
                ):  # if left arrow pressed and cursor is not at far left
                    csr -= 1  # move cursor back
                # same as above but for right arrow
                elif val.code == 261 and csr < len(num):
                    csr += 1  # move cursor forward
                elif val.code == 343:  # if enter key pressed
                    if not valid:  # if number is invalid
                        # write invalid next to the prompt
                        print(
                            f"{_.move_up}{_.move_x(len(prompt)+2)}{_.red}Input invalid{_.normal}",
                            end="",
                        )
                        sys.stdout.flush()
                        time.sleep(0.7)  # wait a bit
                        # get rid of the 'Input invalid'
                        print(f"{_.move_left(13)}{' ' * 13}")
                        sys.stdout.flush()
                    else:
                        # Clear the input and prompt then print the number
                        print(
                            f"{_.move_x(0)}{_.clear_eol}{_.move_up}{_.clear_eol}{_.lightgreen}{num}{_.normal}"
                        )
                        # cast the input to the specified type and return
                        return number_type(num)
                # if the inputted character is a digit or a dot
                elif val in list(string.digits + ".-") and len(num) < _.width:
                    # add it at the cursor position
                    num = num[:csr] + val + num[csr:]
                    csr += 1  # move the cursor forward
                try:
                    i = number_type(num)  # cast the input to the desired type
                    if check(i):
                        if start == None and end == None:  # if there are no bounds
                            valid = True
                        else:
                            if (
                                start != None
                                and end != None
                                and i >= start
                                and i <= end
                            ):
                                valid = True
                            elif start != None and end == None and i >= start:
                                valid = True
                            elif end != None and start == None and i <= end:
                                valid = True
                            else:
                                valid = False
                    else:
                        valid = False
                except:  # the input couldn't be casted
                    valid = False
                # print the inputted number out and move the terminal cursor to its correct position
                print(
                    f"{_.lightgreen if valid else _.red}{_.move_x(0)}{num}{_.normal}{' ' * (_.width - len(num))}{_.move_x(csr)}",
                    end="",
                )
                sys.stdout.flush()

    def confirm(self):
        _ = self.terminal

        with _.cbreak(), _.hidden_cursor():
            ret = True
            while True:
                print(
                    f"{_.lightgreen if ret else ''}True {_.lightgreen if not ret else _.normal}False{_.normal}{_.move_left(10)}",
                    end="",
                )
                sys.stdout.flush()
                val = _.inkey()
                if val.code == 343:  # if enter key pressed
                    break
                if val.code == 260 or val.code == 261:
                    ret = (
                        not ret
                    )  # No matter which arrow key you pressed it will still move to the other option, when there are only 2
        print(f"{_.clear_eol}{_.lightgreen if ret else _.red}{ret}{_.normal}")
        return ret
