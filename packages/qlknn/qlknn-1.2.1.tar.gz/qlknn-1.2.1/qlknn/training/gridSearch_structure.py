import json
from qlknn.training import train_NDNN
import os

if __name__ == "__main__":

    # Different values to test the number of layers parameter for
    # values_to_search_layers = [1, 2, 3, 4, 5]
    #
    # # Different values to test the number of neurons parameter for
    # values_to_search_neurons = [50, 100, 128, 150, 175]
    #
    # # Gives the NN id
    # counter = 0
    #
    # # Train one NN for each L2 param value and save it in the networks folder
    # for i in values_to_search_layers:
    #     for j in values_to_search_neurons:
    #         with open("./settings.json", "r+") as jsonFile:
    #             data = json.load(jsonFile)
    #             hidden_neurons = []
    #             for layer in i:
    #                 hidden_neurons.append(j)
    #             data["hidden_neurons"] = hidden_neurons
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
            rms = data["_metadata"]["rms_validation"]
            print("RMS of ", networkFile, ": ", str(rms))
            networks[networkFile] = rms

    bestNN = min(networks, key=networks.get)
    path = "./networks/" + bestNN
    with open(path, "r") as jsonFile:
        data = json.load(jsonFile)
        hidden_neurons = data["_parsed_settings"]["hidden_neurons"]

    print("Best NN has #neurons param: " + str(hidden_neurons[0]))
    print("Best NN has #layers param: " + str(len(hidden_neurons)))



