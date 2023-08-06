import re 
import pandas as pd

operator_dict = {"*": (lambda x,y: x*y),
    "/": (lambda x,y: x/y),
    "+": (lambda x,y: x+y),
    "-": (lambda x,y: x-y),
    }

def remove_non_operators(equation,operator_dict=operator_dict):
    equation_only_operators=list(map(lambda x:x if type(x)==str and x in list(operator_dict.keys())+["(",")"] else None, equation))
    return equation_only_operators
    
def find_innermost_parentheses_indexes(equation):
    equation_only_operators=remove_non_operators(equation)
    parentheses_count_array=[0 for x in equation_only_operators]
    parentheses_sum=0
    for ind, val in enumerate(equation_only_operators):
        if val=='(':
            parentheses_sum=parentheses_sum+1
            parentheses_count_array[ind]=parentheses_sum
        elif val==')':
            parentheses_sum=parentheses_sum-1
            parentheses_count_array[ind]=parentheses_sum
        else:
            parentheses_count_array[ind]=0
    left_index=parentheses_count_array.index(max(parentheses_count_array))
    right_index=find_closing_parenthesis(left_index,equation_only_operators)
    return (left_index,right_index) if sum(parentheses_count_array)!=0 else (None,None)

def find_closing_parenthesis(start_index,equation_only_operators):
    if equation_only_operators[start_index]=="(":
        count=1
        for index, value in enumerate(equation_only_operators[start_index+1:]):
            if value=="(" :
                count=count+1 
            elif value==")":
                count=count-1
            if count==0:
                return index+start_index+1
                break
    else:
        print("warning: index not an opening parenthesis")

def solver(equation, features_df, operator, operator_dict=operator_dict):
    equation_only_operators=remove_non_operators(equation)
    while equation_only_operators.count(operator)> 0:
        operator_ind=equation_only_operators.index(operator)
        left_ind,right_ind=operator_ind-1,operator_ind+1
        left_string,right_string=equation[left_ind],equation[right_ind]
        left_series=features_df[left_string] if type(left_string)==str else left_string
        right_series=features_df[right_string] if type(right_string)==str else right_string
        result=operator_dict[operator](left_series,right_series)
        del equation[left_ind : right_ind+1]
        equation.insert(left_ind, result)
        equation_only_operators=remove_non_operators(equation)
    return equation

def transform_negative_to_positive(equation,features_df):
    equation_only_operators=remove_non_operators(equation)
    if equation_only_operators.count("-")> 0:
        operator_ind=equation_only_operators.index("-")
        feature_index=operator_ind+1
        feature_name=equation[feature_index]
        feature_series=-features_df[feature_name]
        del equation[feature_index-1 : feature_index+1]
        equation.insert(feature_index-1, feature_series)

        if (feature_index-2)>=0 and equation[feature_index-2] != "(":
            equation.insert(feature_index-1, "+")
        equation_only_operators=remove_non_operators(equation)

    return equation

def calculate(equation, features_df,operator_dict=operator_dict):
    while True:
        left,right=find_innermost_parentheses_indexes(equation)
        if left==None and right==None:
            for operator in operator_dict.keys():
                equation=solver(equation,features_df,operator)
        else:
            subequation=equation[left+1:right]
            for operator in operator_dict.keys():
                subequation=solver(subequation,features_df,operator)
            del equation[left : right+1]
            equation.insert(left, subequation[0])
            
        if len(equation)==1:
            if type(equation[0])==str:
                equation[0]=features_df[equation[0]]
            break
    return equation[0]

def transform(equations_dict, features_df):
    engineered_df = pd.DataFrame()
    for row in equations_dict.items():
        feature_name,equation_string=row
        equation=list(filter(None, re.split(r"([-*+/()])", equation_string)))
        equation=transform_negative_to_positive(equation,features_df)
        engineered_df[feature_name]=calculate(equation,features_df)
    return engineered_df