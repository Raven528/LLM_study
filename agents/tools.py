
# Step 1: Define the available functions in a dictionary
def search_baidu(keyword):
    return f"{keyword}是一个技术博主"

def search_google(keyword):
    return f"{keyword}很牛"

def search_bing(keyword):
    return f"{keyword}喜欢水鱼"

# Function map to easily look up function by name
available_functions = {
    "search_baidu": search_baidu,
    "search_google": search_google,
    "search_bing": search_bing
}

# Step 2: Define the function schema (parameter definitions) in a separate structure
function_schemas = {
    "search_baidu": {
        "type": "function",
        "function": {
            "name": "search_baidu",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                    }
                },
                "required": ["keyword"],
            }
        }
    },
    "search_google": {
        "type": "function",
        "function": {
            "name": "search_google",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                    }
                },
                "required": ["keyword"],
            }
        }
    },
    "search_bing": {
        "type": "function",
        "function": {
            "name": "search_bing",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                    }
                },
                "required": ["keyword"],
            }
        }
    }
}
