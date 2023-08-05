
# Getting Started
***
1. C++ Build Tools (in case not already on your machine - frequently seen with Windows Users)
[download here](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

2. Create a project folder 

    `mkdir covey`

3. Using the terminal of your choice, create a virtual python environment within `covey`.

    `python3 -m venv env`
    
4. Activate the virtual environment. 

    windows `source env/Scripts/Activate` 

    mac `source env/bin/activate` 

5. Once the environment is activated (the terminal should have the environment name pop up in front of the user name as **(env)**), proceed to install the covey-sdk.
    `pip install covey-sdk`

6. Create a new file called test.py or whichever name you would prefer and run the following code

    `import covey.covey_trade as ct`

    `t = ct.Trade(address = <public wallet key>, address_private = <private_wallet_key>, posting_only = True)`

    `t.post_trades_polygon('FB:0.25,ETHUSDT:0.15,AMZN:0.0')`

7. Note the post trades string needs to be one string with the format *<ticker>:<target_percent>,<ticker>:<target_percent>,...*

If successful, the terminal should write back that your trades have been posted.

Please let us know if you have any questions or run into issues, happy coding!

# FAQs
*** 
* target_percent is the new percent you want the size to be. If you had a prior target_percent of 0.01 (1%), then you added a new target_percent of 0.03 (3%) that would buy you an additional (0.02) 2%. So the end position is 0.03 (3%)
* To close a position you need to run target_percent = 0.0