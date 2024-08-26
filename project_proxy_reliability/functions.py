import asyncio

"Functions to manage the main"

async def print_proxy_managers(list,arg):
    for proxy_manager_item in list:
        await proxy_manager_item.print_proxy_list(arg)
        

async def sort_proxy_managers(list,proxy_number):
    for proxy_manager_item in list:
        await proxy_manager_item.sort_proxy_lists(proxy_number)

def reset_proxy_objects(list):
    for proxy_manager_item in list:
        proxy_manager_item.reset_proxys() #resets the proxy attributes, logs the score, copys master -> proxy_list, clears master list

def log_scores(list):
    for proxy_manager_item in list:
        proxy_manager_item.log_scores() #Store Scores before Reset


"Function to fulfill dynamic approach - Re-Evaluate every 20s, remove not reliable Proxys with avg_score < 100 and add new reliable Proxys with Score >= 100"
async def rec_wait_and_evaluate_again(proxy_managers_list, counter, evaluation_rounds,proxy_number,num_proto,stop_counter):
    stop_counter += 1
    log_scores(proxy_managers_list) #Log Score here before reset AND remove avg_score <= 100
    await print_proxy_managers(proxy_managers_list,"master")
    print("\n\n      ------- Initiated Termination -------\n\n     ^                                         ^\n     |   Here is the final Master Proxy List   |\n")

    print("Wait 20s until Master List re-evaluate. Press ctrl + z to break and show the final List.\n")
    
    for _ in range(20):  # 20 Seconds / 2 Seconds = 10
        
        await asyncio.sleep(1)
            
        print('.', end='',flush=True)
    
    
    print('\nEvaluate Master List again!\n')

    #TODO refresh the list with reliable proxys still not refilling enough proxys.
    
    re_refresh_tasks = []
    await Checker(proxy_managers_list,re_refresh_tasks,proxy_number,num_proto,counter,num_proto)

    reset_proxy_objects(proxy_managers_list) # reset proxy Objects and init Master/Proxy List for new evaluation Update

    re_evaluate_tasks = await generate_evaluate_tasks(proxy_managers_list, counter, evaluation_rounds,proxy_number)
    
    await asyncio.gather(*re_evaluate_tasks)
    await sort_proxy_managers(proxy_managers_list,proxy_number)
    #await print_proxy_managers(proxy_managers_list,"master")
    
    if stop_counter != 6:
        await rec_wait_and_evaluate_again(proxy_managers_list,counter,evaluation_rounds,proxy_number,num_proto,stop_counter)
    
    else: return
    
async def generate_evaluate_tasks(proxy_managers_list, counter, evaluation_rounds,proxy_number):
    re_evaluate_tasks = []
    for manager in proxy_managers_list:
        re_evaluate_tasks.append(manager.evaluate_proxy_list(counter, evaluation_rounds,proxy_number))
        
    return re_evaluate_tasks

async def generate_refresh_tasks(proxy_managers_list, counter, evaluation_rounds,proxy_number):
    re_refresh_tasks = []
    for manager in proxy_managers_list:
        re_refresh_tasks.append(manager.refresh_proxy_list(counter,proxy_number,evaluation_rounds ))
        
    return re_refresh_tasks

async def Checker(proxy_managers_list,refresh_tasks:list,proxy_number,num_proto,counter,evaluation_rounds):
    unbalanced = True

    while unbalanced:

        
        print("CHECKER ACTIVE\n")
        await asyncio.sleep(3)
        
        checked = []
        for items in proxy_managers_list:
            
            if len(items.master_proxy_list) == proxy_number:
                    checked.append(1)
            else:
                items.ready_for_connection = False
                

        if checked.count(1) == num_proto:

            print("CHECK APPROVED - CONTINUE\n")
            await asyncio.sleep(5)
            unbalanced = False
            
        else:
            print("CHECK REJECT - REFILL\n")
            await asyncio.sleep(5)
            refresh_tasks = await generate_refresh_tasks(proxy_managers_list, counter, evaluation_rounds,proxy_number)
            await asyncio.gather(*refresh_tasks)
            

        checked.clear()