import os
import xml.etree.ElementTree as ET
import pandas as pd

# File paths
input_file_path = r"C:\Users\*****.xml" # Put the file directory here
output_directory = r"C:\Users\******" # Put the output directory here
output_file_path = os.path.join(output_directory, "*****.csv") # Put the output file path here

# Threshold for pauses (in milliseconds)
PAUSE_THRESHOLD = 1000  # 0.1 seconds

# Function to parse the XML file and extract events and final text
def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    events = []
    for event in root.findall('.//Key'):
        events.append({
            'time': int(event.get('Time')),
            'type': event.get('Type'),
            'value': event.get('Value')
        })
    
    final_text = root.find('.//FinalTextUTF8').text
    return events, final_text

# Function to calculate pauses within and between words
def calculate_pauses(events, words):
    results = []
    index = 0
    for word in words:
        word_length = len(word)
        word_events = events[index:index + word_length]
        index += word_length
        
        # Calculate pauses within the word
        pauses_within = []
        for i in range(1, len(word_events)):
            pause = word_events[i]['time'] - word_events[i-1]['time']
            if pause >= PAUSE_THRESHOLD:
                pauses_within.append(pause)
        
        total_pause_within = sum(pauses_within)
        pause_count_within = len(pauses_within)
        
        # Calculate pause between words
        if index < len(events):
            next_event_time = events[index]['time']
            last_event_time = word_events[-1]['time']
            pause_between = next_event_time - last_event_time
            if pause_between >= PAUSE_THRESHOLD:
                total_pause_between = pause_between
                pause_count_between = 1
            else:
                total_pause_between = 0
                pause_count_between = 0
        else:
            total_pause_between = 0
            pause_count_between = 0
        
        results.append({
            'word': word,
            'pause_count_within': pause_count_within,
            'total_pause_within': total_pause_within,
            'pause_count_between': pause_count_between,
            'total_pause_between': total_pause_between
        })
    
    return results

# Main function to execute the script
def main(input_file, output_file):
    events, final_text = parse_xml(input_file)
    words = final_text.split()
    
    results = calculate_pauses(events, words)
    
    # Convert results to DataFrame
    df = pd.DataFrame(results)
    
    # Save DataFrame to CSV
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"Output saved to {output_file}")

if __name__ == "__main__":
    main(input_file_path, output_file_path)
