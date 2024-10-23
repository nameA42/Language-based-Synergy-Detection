import sys
from openai import OpenAI
from auth import OpenAI_AUTH

#     (10:32)   (10:42)
# test  6.93  ->  2.62

if __name__=="__main__":
    if len(sys.argv) < 2:
        raise Exception("Action not defined")
    action = sys.argv[1]
    client = OpenAI(api_key=OpenAI_AUTH)
    if action == 'check':
        if len(sys.argv) < 3:
            raise Exception("Batch id not provided (submit the batch and use the id here)")
        batch = client.batches.retrieve(sys.argv[2])
        print("Status: ", batch.status)
        print("Output file id: ", batch.output_file_id)
        print(batch)
    elif action == 'retrieve':
        if len(sys.argv) < 3:
            raise Exception("Result file id not provided (check your batch, and use the output_file_id here)")
        if len(sys.argv) < 4:
            raise Exception("Output filename not specified")
        file_response = client.files.content(sys.argv[2])
        with open(sys.argv[3], 'a') as outfile:
            print(file_response.text, file=outfile)
        print(f"Logged in {sys.argv[3]}")
    elif action == 'cancel':
        if len(sys.argv) < 3:
            raise Exception("Batch id not provided (submit the batch and use the id here)")
        print(client.batches.cancel(sys.argv[2]))
    elif action == 'list':
        l = client.batches.list(limit=6)
        print("id\t\t\t\t\tstatus\t\toutput_filename")
        for entry in l.data:
            print(f"{entry.id}\t{entry.status}\t{entry.output_file_id}")
        if l.has_more: # type: ignore for some reason this is not in the schema??
            print('...')
    elif action == 'submit':
        if len(sys.argv) < 3:
            raise Exception("Filename not provided")
        filename = sys.argv[2]
        inp = input("Please confirm sending this batch by writing \"confirm\".")
        if inp != "confirm":
            raise Exception("Action not confirmed")
        batch_input_file = client.files.create(
            file=open(filename, "rb"),
            purpose="batch"
        )
        batch_input_file_id = batch_input_file.id
        print("batch id: ", batch_input_file.id)
        batch = client.batches.create(
            input_file_id=batch_input_file_id,
            endpoint="/v1/chat/completions",
            completion_window="24h",
            metadata={
                "description": f"Synergy Evaluation Job - {filename}"
            }
        )
        print(batch)
        with open(f'batch_history.log', 'a') as outfile:
            print(batch, file=outfile)
            outfile.write('\n---\n')
        print("submitted and added to batch_history.log")
    else:
        raise Exception("Action not recognized")
