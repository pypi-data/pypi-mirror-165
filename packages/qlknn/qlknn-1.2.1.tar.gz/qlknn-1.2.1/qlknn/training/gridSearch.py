import json
from qlknn.training import train_NDNN
import os

if __name__ == "__main__":

    # # Different values to test the L2 parameter for
    # values_to_search_L2 = [0.000005, 0.00005, 0.0005, 0.005, 0.1]
    #
    # # Different values to test the batch size parameter for
    # # values_to_search_bs = [100, 500, 1000, 5000, 10000]
    # values_to_search_bs = [10000, 5000, 1000, 500, 100]
    #
    # # Gives the NN id
    # counter = 0
    #
    # # Train one NN for each L2 param value and save it in the networks folder
    # for i in values_to_search_L2:
    #     for j in values_to_search_bs:
    #         with open("./settings.json", "r+") as jsonFile:
    #             data = json.load(jsonFile)
    #             data["cost_l2_scale"] = i
    #             data["minibatches"] = j
    #             jsonFile.seek(0)  # rewind
    #             json.dump(data, jsonFile, indent=2)
    #             jsonFile.truncate()
    #         counter += 1
    #
    #         train_NDNN.train_NDNN_from_folder2(counter)
    # print("Finished training all NNs")

    # Retrieve the NN with the smallest Root Mean Square Error
    networks = {}
    for networkFile in os.listdir("./networks/"):
        path = "./networks/" + networkFile
        with open(path, "r") as jsonFile:
            data = json.load(jsonFile)
            #l2 = data["_parsed_settings"][]
            rms = data["_metadata"]["rms_test"]
            print("RMS of ", networkFile, ": ", str(rms))
            networks[networkFile] = rms

    bestNN = min(networks, key=networks.get)
    path = "./networks/" + bestNN
    with open(path, "r") as jsonFile:
        data = json.load(jsonFile)
        l2 = data["_parsed_settings"]["cost_l2_scale"]
        batch_size = data["_parsed_settings"]["minibatches"]

    print("Best NN has L2 param: " + str(l2))
    print("Best NN has batch size param: " + str(batch_size))



