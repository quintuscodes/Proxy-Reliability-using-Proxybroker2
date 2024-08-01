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

async def rec_wait_and_evaluate_again(proxy_managers_list, counter, evaluation_rounds,proxy_number):
    log_scores(proxy_managers_list) #Log Score here before reset TODO: Not correct
    await print_proxy_managers(proxy_managers_list,"master")
    print("\n\n      ------- Initiated Termination -------\n\n     ^                                         ^\n     |   Here is the final Master Proxy List   |\n")

    print("Wait 40s until Master List re-evaluate. Press ctrl + z to break and show the final List.\n")
    
    for _ in range(20):  # 40 Seconds / 2 Seconds = 20
        
        await asyncio.sleep(2)
            
        print('.', end='',flush=True)
    
    
    print('\nEvaluate Master List again!\n')

    
    reset_proxy_objects(proxy_managers_list) # reset proxy Objects and init Master/Proxy List for new evaluation Update

    re_evaluate_tasks = await generate_evaluate_tasks(proxy_managers_list, counter, evaluation_rounds,proxy_number)
    
    await asyncio.gather(*re_evaluate_tasks)
    await sort_proxy_managers(proxy_managers_list,proxy_number)
    await print_proxy_managers(proxy_managers_list,"master")
    await print_proxy_managers(proxy_managers_list,"slave")
    
    await rec_wait_and_evaluate_again(proxy_managers_list,counter,evaluation_rounds,proxy_number)
    
    
async def generate_evaluate_tasks(proxy_managers_list, counter, evaluation_rounds, proxy_number):
    re_evaluate_tasks = []
    for manager in proxy_managers_list:
        re_evaluate_tasks.append(manager.evaluate_proxy_list(counter, evaluation_rounds, proxy_number))
    return re_evaluate_tasks

async def Checker(proxy_managers_list,refresh_tasks,proxy_number,num_proto):
    unbalanced = True
    while unbalanced:

        await asyncio.sleep(5)
        print("CHECKER METHOD active\n")
        
        await print_proxy_managers(proxy_managers_list,0)
        
        await print_proxy_managers(proxy_managers_list,"master")
        await asyncio.sleep(5)

        print(f"Query new reliable Proxys to MASTER List ")

        "Remove/Add here desired protocols"
        
        await asyncio.gather(*refresh_tasks)
        
        "Remove/Add here desired protocols in if - statement"
        checked = []
        for items in proxy_managers_list:
            
            if len(items.master_proxy_list) == proxy_number:
                    checked.append(1)

        if checked.count(1) == num_proto:
            print("CHECK approved")
            await asyncio.sleep(5)

            unbalanced = False
            
        else:
            print("Notdoneyet")
            await asyncio.sleep(5)

