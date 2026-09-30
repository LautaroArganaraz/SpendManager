import sqlite3 as sq

import numpy as np
import pandas as pd
import streamlit as st


#This will tell if the transaction is positive or negative
def calculate_amount(type: str, amount: float) -> float:
    if type == "Income":
        return amount * 1
    else:
        return amount * -1

#This calls the database to check the actual balance
def total_balance(transactions: pd.DataFrame) -> float:
    return transactions['Amount'].sum()