import os
import logging
import torch
import LTCArchitecture as ltc
import Preprocessor
import pandas as pd

# Set up logging
logger = logging.getLogger(__name__)

def get_state():
    try:
        current_dir = os.path.dirname(__file__)
        state_file_path = os.path.join(current_dir, "state.txt")
        logger.debug(f"Looking for state.txt at: {state_file_path}")
        
        if not os.path.exists(state_file_path):
            logger.error(f"state.txt not found at {state_file_path}")
            return {"error": "State file not found"}
            
        encodings = ['utf-8', 'utf-16', 'ascii']
        for encoding in encodings:
            try:
                with open(state_file_path, "r", encoding=encoding) as file:
                    lines = file.readlines()
                    if not lines:
                        logger.warning("state.txt is empty")
                        return {"error": "State file is empty"}
                    
                    logger.debug(f"Successfully read file with {encoding} encoding")
                    return get_line_result(lines, len(lines) - 1)
            except UnicodeError:
                continue
            
        return {"error": "Could not read file with any known encoding"}
    except Exception as e:
        logger.error(f"Error reading state: {str(e)}", exc_info=True)
        return {"error": str(e)}

def get_history(count):
    try:
        logger.debug(f"Attempting to get history for count: {count}")
        current_dir = os.path.dirname(__file__)
        state_file_path = os.path.join(current_dir, "state.txt")
        
        with open(state_file_path, "r") as file:
            lines = file.readlines()
            if not lines:
                logger.warning("state.txt is empty")
                return []

            line_count = len(lines)
            if line_count < count:
                count = line_count

            results = []
            start_index = max(0, line_count - count)
            
            for i in range(start_index, line_count):
                try:
                    result = get_line_result(lines, i)
                    result["index"] = i - start_index
                    results.append(result)
                except Exception as e:
                    logger.error(f"Error processing line {i}: {str(e)}")
                    continue

            return results
    except Exception as e:
        logger.error(f"Error in get_history: {str(e)}", exc_info=True)
        return []

def get_line_result(lines, index):
    try:
        current_state = lines[index].strip().split(",")
        if len(current_state) != 12:
            logger.error(f"Invalid data format in state.txt at line {index}")
            return create_empty_state()

        result = {
            "index": index,
            "nature": float(current_state[0]),
            "intensity": float(current_state[1]),
            "month": float(current_state[2]),
            "day": float(current_state[3]),
            "hour": float(current_state[4]),
            "lat": float(current_state[5]),
            "lon": float(current_state[6]),
            "wind": float(current_state[7]),
            "pres": float(current_state[8]),
            "gust": float(current_state[9]),
            "eye": float(current_state[10]),
            "speed": float(current_state[11])
        }
        return result
    except Exception as e:
        logger.error(f"Error processing line: {str(e)}")
        raise

def load_model():
    features = 10
    outputs = 2

    neurons = 700
    theta = 450
    tau = 20

    model = ltc.ReadOut(features, neurons, theta, tau, outputs)
    model.load_state_dict(torch.load('model.pth'))
    model.to(device)
    model.eval()
    return model


device = (
        "cuda"
        if torch.cuda.is_available()
        else "mps"
        if torch.backends.mps.is_available()
        else "cpu"
    )
