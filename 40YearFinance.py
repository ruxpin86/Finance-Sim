
import random

#TODO: let the user choose time horizon and work on cleaning up output instruction
user_name = input("What is your name?: ")
print()
print(f"Welcome to the 40 year financial simulator game {user_name}!\n")
print("You are beginning your investment journey with $2,000.00 in a high yield savings account.\n" \
"How much can you achieve in returns after 40 years?")
print("Your portfolio is comprised of 5 investment types:\n" \
"1--> Bonds which can yield -2% - +9% annually --------------------------> (LOW RISK)\n" \
"2--> Exchange Traded Funds (ETFs) that can yield -8% - +25% annually ---> (MODERATE RISK)\n" \
"3--> Individual Stocks which can yield -20% - +40% annually ------------> (HIGH RISK)\n" \
"4--> Cryptocurrency or 'Crypto' that can yield -50% - +70% annually ----> (VERY HIGH RISK)\n"
"5--> High Yield Savings Account (HYSA) which yields 2% - +4% annually --> (NO RISK)\n\n")

#asks the user how they would like to spread their funds across the pre-defined assets
def get_user_allocations(portfolio_balance):
    print(f"How do you want to spread your current portfolio value of ${portfolio_balance:,.2f} across your asset options?\n")
    print(f"Enter a  number between 0-100 to indicate the percentage you would like to allocate to each when prompted.")
    print(f"You cannot exceed the remaining allocation percentage.\n")
    print(f"NOTE: Any unallocated remaining percentage funds after entering disbursement will automatically be put into your HYSA,\n"\
    "and it is smart to always keep some of your funds in a secure asset as a reserve.\n")
    remaining_percentage = 100
    user_allocations = []

    #list of tuples to be called when prompting the user so there's no repetition.
    user_prompts = [
        ("Bond (LOW RISK)", "Bonds"),
        ("ETFs (MODERATE RISK)", "ETFs"),
        ("Individual stocks (HIGH RISK)", "Stocks"),
        ("Cryptocurrency (VERY HIGH RISK)", "Crypto")
    ]
    #looping through user_prompts to get each percentage input from the user
    for i in range(len(user_prompts)):
        prompt, name = user_prompts[i] #unpacking the list of tuples into seperate pieces to be used in the output

        #input validation loop to check 1st: is the input able to be converted to a float 2nd: does the float fall in the range of the percent remaining to allocate
        while True:
            print(f"You have {remaining_percentage}% left to divide across your assets.")
            user_input = input(f"How much would you like to allocate to {prompt}?: ")
            print() #blank line for readability in the terminal
            #checking that the input is a number that can be converted to a float
            try:
                user_input = float(user_input)
            except ValueError:
                print("ERROR: Not a valid percentage input")
                continue #invalid input restarts the loop
            #checking if the input is between 0 and remaining_remaining percentage
            if user_input < 0 or user_input > remaining_percentage:
                print("ERROR: Input not within the remaining range to be allocated")
                continue #invalid input restarts the loop

            #converting user input to a decimal, adding it to the list user_allocations, subtracting user_input to update remaining_percentage 
            user_input_as_decimal = user_input * .01
            user_allocations.append(user_input_as_decimal)
            remaining_percentage -= user_input
            
            break #exiting the 'while' loop

    #final output to display the breakdown of user_input to the user
    print(("=" * 25) + "PORTFOLIO ALLOCATION BREAKDOWN" + ("=" * 25))
    #formatting output to be more readable with dot "." to guide users eye to asset amount
    for i in range(len(user_prompts)):
        prompt, name = user_prompts[i]
        label = name + ":"
        formatted_percentage = f"{user_allocations[i] * 100:.2f}%"
        line_width = 69
        dots_needed = line_width - (len(label) + 1) - (len(formatted_percentage) + 1)
        dots = "."
        print(f"{label} {dots * dots_needed} {formatted_percentage}")

    print()
    print(f"The remaining {remaining_percentage}% will be put into your HYSA\n")
    user_allocations.append(remaining_percentage * .01)

    return user_allocations

# Takes the users inputted allocation percentages and then returns the dollar value 
# based on that input into the list account_balances
def allocate_initial_balances(allocations, portfolio_balance):
    asset_balances =[]
    for i in allocations:
        asset_balances.append(i * portfolio_balance)
    
    return asset_balances

#gets a monthly contribution amount from the user and then splits that apart by previously stored user_allocations
def add_monthly_contribution(user_allocations):
    monthly_contribution_list = []
    print("Continuing to invest beyond your initial contribution is critical if you want to see meaningful returns over time.\n" \
    "This super charges your portfolio and really allows you to leverage the power of compound interest over time!!!")
    #get contribution input, then check input is valid by attempting to convert it to a float
    while True:
        monthly_contribution_amount = input("How much would you like to contribute to your investment portfolio every month? (enter a dollar amount): ")
        print()
        try:
            monthly_contribution_amount = float(monthly_contribution_amount)
        except ValueError:
            print("ERROR: Not a valid input type.")
            continue
        #once validated, convert that using the allocation percentage, round the result to avoid floating-point noise, append to monthly_contribution_list
        for i in range(len(user_allocations)):
            allocated_amount = user_allocations[i] * monthly_contribution_amount
            rounded_allocated_amount = round(allocated_amount, 2)
            monthly_contribution_list.append(rounded_allocated_amount)
        
        break
        
    return monthly_contribution_list
        

# rebalances portfolio after 10 years back to their original percentage allocations
def rebalance_every_10th_year(portfolio_balance, asset_balances, allocations, asset_list):
    year_by_10 = [10, 20, 30, 40] #this has to be in the main function and then looped through and passed as an argument, something to work on later for better output
    new_asset_balances = []
    print(f"Your portfolio balance after the past decade is now ${portfolio_balance:,.2f}")
    print(("=" * 25) + "PORTFOLIO BREAKDOWN" + ("=" * 25))

    for asset in range(len(asset_balances)):
        name = asset_list[asset]
        balance = asset_balances[asset]
        balance_length = (len(f"${balance:,.2f}"))
        percent = (balance / portfolio_balance) * 100 
        line_width = 50
        dots = "."
        dots_needed = line_width - (len(name) +balance_length)
        print(f"{name} {dots * dots_needed} ${balance:,.2f} ... {percent:.2f}%")
    print()
    for i in range(len(allocations)):
        new_asset_balances.append(portfolio_balance * allocations[i])

#TODO: put in an output for what the portfolio will look like once it is rebalanced

    return new_asset_balances

#this will determine the state behavior of an event by rolling probability to see if it has occurred
def roll_random_event(counters):
    random_events = {
        "pandemic": False,
        "recession": False,
        "tech surge": False,
        "favorable election": False,
        "crypto crash": False,
        "LIR": False,
    }

    #'pandemic' event roll
    if counters["recession_pandemic_blocked_years_remaining"] == 0:
        roll = random.random()
        if roll <= 0.03:
            random_events["pandemic"] = True

    #'recession' event roll
    if counters["recession_pandemic_blocked_years_remaining"] == 0:
        roll = random.random()
        if random_events["pandemic"] == True:
            if roll <= 0.33:
                random_events["recession"] = True
        else:
            if roll <= 0.25:
                random_events["recession"] = True
    
    #'tech-surge' event roll
    if counters["tech_surge_blocked_years_remaining"] == 0:
        roll = random.random()
        if random_events["recession"] == True:
            random_events["tech surge"] = False
        else:
            if roll <= .20:
                random_events["tech surge"] = True

    #'favorable election' event roll
    if counters["election_year_interval"] == 0:
        roll = random.random()
        if roll <= .50:
            random_events["favorable election"] = True
            #what happens if the election occurs during a 'recession' event?
    
    #'crypto crash' event roll
    if counters["crypto_crash_blocked_years_remaining"] == 0:
        roll = random.random()
        if random_events["favorable election"] == True:
            random_events["crypto crash"] = False
        else:
            if roll <= 0.25:
                random_events["crypto crash"] = True

    #checking LIR condition
    if counters["LIR_years_remaining"] == 0 and random_events["pandemic"] == True:
        random_events["LIR"] = True
    if counters["LIR_years_remaining"] == 0 and random_events["recession"] == True:
        random_events["LIR"] = True

    print(f"RANDOM EVENTS: {random_events}")

    return random_events

#function to handle the counter cool-downs so that events are rolled only when their effects have worn off
def update_event_counters(counters, events):
    #decrement an active event counter
    for key in counters:
        if counters[key] > 0:
            counters[key] -= 1
    
    if events["pandemic"] == True:
        counters["recession_pandemic_blocked_years_remaining"] = 6
        counters["tech_surge_blocked_years_remaining"] = 1
        counters["LIR_years_remaining"] = 3
    
    if events["recession"] == True:
        counters["recession_pandemic_blocked_years_remaining"] = 6
        counters["tech_surge_blocked_years_remaining"] = 1
        counters["LIR_years_remaining"] = 3

    if events["favorable election"] == True:
        counters["crypto_crash_blocked_years_remaining"] = 1
        counters["recession_pandemic_blocked_years_remaining"] = 1
    
    if counters["election_year_interval"] == 0:
        counters["election_year_interval"] = 3

    return counters

#function to apply effects to assets if event rolls True for a given year
def apply_random_event_effects(events, event_counters, base_return_ranges):
    print(f"BASE RETURNS: {base_return_ranges}")
    modified_return_range = base_return_ranges[:]

    #LIR needs to be a regime change that is accounted for before shocks are factored in by the function
    if event_counters["LIR_years_remaining"] > 0: #bonds become safer, and better returns
        bond_low, bond_high = modified_return_range[0] 
        modified_return_range[0] = bond_low + 0.01, bond_high + 0.05

    if events["pandemic"] == True:
        for i in range(1, len(base_return_ranges) - 1):
            low, high = modified_return_range[i]
            modified_return_range[i] = (low - 0.35, high - 0.10)
    
    if events["recession"] == True:
        for i in range(1, len(base_return_ranges) - 1):
            low, high = modified_return_range[i]
            modified_return_range[i] = (low - 0.15, high - 0.05)

    #tech surge effect
    if events["tech surge"] == True:
        #modify etf returns
        etf_low, etf_high = modified_return_range[1]
        modified_return_range[1] = (etf_low + 0.08, etf_high + 0.15)
        #modify stocks returns
        stocks_low, stocks_high = modified_return_range[2]
        modified_return_range[2] = (stocks_low + 0.20, stocks_high + 0.08)
    
    #favorable election effect
    if events["favorable election"] ==True:
        etf_low, etf_high = modified_return_range[1]
        modified_return_range[1] = (etf_low + 0.08, etf_high + 0.12)

        stocks_low, stocks_high = modified_return_range[2]
        modified_return_range[2] = (stocks_low + 0.20, stocks_high + 0.08)
    
    #crypto crash effect
    if events["crypto crash"] == True:
        crypto_low, crypto_high = modified_return_range[3]
        modified_return_range[3] = (crypto_low - 0.10, crypto_high - 0.70)

    print(f"THIS YEARS RETURNS: {modified_return_range}")

    return modified_return_range

# simulates a single year of compounding by looping through each asset and updating it's value
def sim_one_year(asset_balances, year, yearly_return_ranges):
    print(f"THIS YEARS RETURN RANGES: {yearly_return_ranges}\n")
    updated_balances = []

    for i in range(len(yearly_return_ranges)):
        low, high = yearly_return_ranges[i] #unpacks the tuple in return_ranges so it's usable with random()
        random_return = random.uniform(low, high) #getting a random number within the specified range
        new_asset_balance = asset_balances[i] * (1 + random_return) #multiply asset_balance by random_return to get growth or loss for the year
        updated_balances.append(new_asset_balance) #assign that updated balance to the list updated_balances

    year += 1 #increment year, duh

    return updated_balances, year

    #TODO: print a yearly summary with percent increases and the amount made in each asset category

#main function to run the program
def main():
    current_year = 0 #initialize the year
    total_years = 40 #set the length/time horizon of the simulation
    starting_balance = 2000 #users balance to start the simulation (this could easily just be zero with the monthly contribution providing the fuel)
    asset_list = ["Bonds", "ETFs", "Stocks", "Crypto", "HYSA"] #List of assets as strings for output
    annual_contribution_list = [] #empty list to assign (monthly_contributions * 12) to store monthly converted to yearly
    event_counters = { #stores the cool-down timers for events per the defined rules
    "recession_pandemic_blocked_years_remaining": 0,
    "tech_surge_blocked_years_remaining": 0,
    "crypto_crash_blocked_years_remaining": 0,
    "election_year_interval": 0,
    "LIR_years_remaining": 0,
    }

    #list of tuples for annual base return rate ranges that can now be changed based on event occurrence
    base_return_ranges = [
    (-0.02, 0.09),  #Bond return range
    (-0.08, 0.25),  #ETF return range
    (-.20, 0.50),   #Stocks return range
    (-0.40, 0.80),  #Crypto
    (0.02, 0.04)    #HYSA
]

    #get user asset allocations
    allocations = get_user_allocations(starting_balance)

    #ask user for monthly contribution amount
    monthly_contributions = add_monthly_contribution(allocations)
    #take the list of monthly_contributions and convert it to an annual_contribution amount, add it to the annual_contributions_list
    for contribution in range(len(monthly_contributions)):
        annual_contribution = monthly_contributions[contribution] * 12
        annual_contribution_list.append(annual_contribution)

    #convert the user input allocation percentages into dollar amounts across the defined starting_balance
    asset_balances = allocate_initial_balances(allocations, starting_balance)

    #add on the annual contribution amounts to each asset class
    portfolio_balance = sum(asset_balances)

    def pre_year_summary(): #I may use this function in the future to provide more output to user, but for now it was a bit much in the terminal
        print(f"{user_name}, this is your current breakdown of allocations and current account values...")
        for i in range(len(asset_balances)):
            print(f"{asset_list[i]} {allocations[i] * 100:.1f}%, {asset_balances[i]:,.2f}")
            
    print(("=" * 10) + "\n" + "YEAR: 0" + "\n" + ("=" * 10)+ "\n")

    for _ in range(total_years):
        #pre_year_summary()
        random_events = roll_random_event(event_counters) #stores the return of roll_random_events() to be passed to update_event_counters()
        update_event_counters(event_counters, random_events) #handle the event counters before applying effects of those events
        yearly_return_ranges = apply_random_event_effects(random_events, event_counters, base_return_ranges)

        asset_balances, current_year = sim_one_year(asset_balances, current_year, yearly_return_ranges)

        print(("=" * 10) + "\n" + "YEAR: " + str(current_year) + "\n" + ("=" * 10)+ "\n")
        for balance in range(len(asset_balances)):
            asset_balances[balance] += annual_contribution_list[balance]
        # print(f"After year {current_year} your accounts are now at:")
        # for i in range(len(asset_balances)):                      THIS CAN ALL BE IGNORED, MAY USE IN THE FUTURE BUT CURRENTLY BLOATING THE OUTPUT
        #     print(f"{asset_list[i]}: {asset_balances[i]:,.2f}") 
        portfolio_balance = sum(asset_balances) #totaling up all assets to output total value of the users portfolio
        # print(f"Total: {portfolio_balance:,.2f}\n")

        #for every decade of the simulation rebalance that portfolio back to the original allocations defined by the user and print breakdown
        if current_year % 10 == 0:
            asset_balances = rebalance_every_10th_year(portfolio_balance, asset_balances, allocations, asset_list)
        
        print(f"EVENT COUNTERS: {event_counters}")
            

    #final output for investment results after defined amount of years... I could have the user define their time horizon to tailor it to their investment goals
    print(f"After year {current_year} your accounts are now at:")
    for i in range(len(asset_balances)):
        print(f"{asset_list[i]}: {asset_balances[i]:,.2f}")
    print(f"Ending portfolio balance: ${portfolio_balance:,.2f}\n")


if __name__ == "__main__":
    main()

#------------------------------TEST LAND------------------------------#

#Testing get_user_allocations()

# portfolio_balance = 2000
# player_allocations = get_user_allocations(portfolio_balance)

# print(player_allocations)

#---------------------------------------

#Testing sum_one_year()

# test_balances = [1000, 1000, 1000, 1000, 1000]  # $1k in each asset
# year = 1

# updated, new_year = sim_one_year(test_balances, year)

# print("UPDATED:", updated)
# print("NEW YEAR:", new_year)

#---------------------------------------

#Testing add_monthly_contribution()
# portfolio_balance = 2000

# allocations = get_user_allocations(portfolio_balance)

# monthly = add_monthly_contribution(allocations)

# print(monthly)

#---------------------------------------

#Testing my roll_random_events() function to see if I am returning booleans correctly for 10 years worth of events
# event_counters = {
# "recession_pandemic_blocked_years_remaining": 0,
# "tech_surge_blocked_years_remianing": 0,
# "crypto_crash_blocked_years_remaining": 0,
# "election_year_interval": 0,
# "LIR_years_remaining": 0,
# }
# for i in range(10):
#     print(roll_random_event(event_counters))