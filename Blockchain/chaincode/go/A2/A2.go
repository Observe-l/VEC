/*
SPDX-License-Identifier: Apache-2.0
*/

package main

import (
	"encoding/json"
	"fmt"
	"strconv"

	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

// SmartContract provides functions for managing a car
type SmartContract struct {
	contractapi.Contract
}

// BaseStation describes basic details of what makes up a car
type BaseStation struct {

	// ID                          string  `json:"id"`
	Global_computing_resource   float64 `json:"global_computing_resource"`
	Reversed_computing_resource float64 `json:"reversed_computing_resource"`
	Computing_efficiency        float64 `json:"computing_efficiency"`
	Completion_ratio            float64 `json:"completion_ratio"`
	Total_received_task         float64 `json:"total_received_task"`
	Reliability                 float64 `json:"reliability"`
}

// QueryResult structure used for handling result of query
type QueryResult struct {
	Key    string `json:"Key"`
	Record *BaseStation
}

// InitLedger adds a base set of basestations to the ledger
func (s *SmartContract) InitLedger(ctx contractapi.TransactionContextInterface) error {
	basestations := []BaseStation{
		BaseStation{Global_computing_resource: 20, Reversed_computing_resource: 10, Computing_efficiency: 0,Completion_ratio:0,Total_received_task:0,Reliability:0},
		BaseStation{Global_computing_resource: 29, Reversed_computing_resource: 0, Computing_efficiency: 1,Completion_ratio:1,Total_received_task:1,Reliability:1},
	}

	for i, basestation := range basestations {
		BSAsBytes, _ := json.Marshal(basestation)
		err := ctx.GetStub().PutState("BASESTATION"+strconv.Itoa(i), BSAsBytes)

		if err != nil {
			return fmt.Errorf("Failed to put to world state. %s", err.Error())
		}
	}

	return nil
}

// CreatS adds a new basestation to the world state with given details
func (s *SmartContract) CreateBS(ctx contractapi.TransactionContextInterface, BSNumber string, global_computing_resource float64, reversed_computing_resource float64, computing_efficiency float64, completion_ratio float64,total_received_task float64,reliability float64) error {
	basestation := BaseStation{
		Global_computing_resource:global_computing_resource,
		Reversed_computing_resource:reversed_computing_resource,
		Computing_efficiency: computing_efficiency,
		Completion_ratio:completion_ratio,
		Total_received_task:total_received_task,
		Reliability:reliability,
	}

	BSAsBytes, _ := json.Marshal(basestation)

	return ctx.GetStub().PutState(BSNumber, BSAsBytes)
}

// QueryBS returns the car stored in the world state with given id
func (s *SmartContract) QueryBS(ctx contractapi.TransactionContextInterface, BSNumber string) (*BaseStation, error) {
	BSAsBytes, err := ctx.GetStub().GetState(BSNumber)

	if err != nil {
		return nil, fmt.Errorf("Failed to read from world state. %s", err.Error())
	}

	if BSAsBytes == nil {
		return nil, fmt.Errorf("%s does not exist", BSNumber)
	}

	basestation := new(BaseStation)
	_ = json.Unmarshal(BSAsBytes, basestation)

	return basestation, nil
}

// QueryAllBSs returns all BSs found in world state
func (s *SmartContract) QueryAllBSs(ctx contractapi.TransactionContextInterface) ([]QueryResult, error) {
	startKey := ""
	endKey := ""

	resultsIterator, err := ctx.GetStub().GetStateByRange(startKey, endKey)

	if err != nil {
		return nil, err
	}
	defer resultsIterator.Close()

	results := []QueryResult{}

	for resultsIterator.HasNext() {
		queryResponse, err := resultsIterator.Next()

		if err != nil {
			return nil, err
		}

		basestation := new(BaseStation)
		_ = json.Unmarshal(queryResponse.Value, basestation)

		queryResult := QueryResult{Key: queryResponse.Key, Record: basestation}
		results = append(results, queryResult)
	}

	return results, nil
}

// UpdataBS updates BS field of car with given id in world state
func (s *SmartContract) UpdataBS(ctx contractapi.TransactionContextInterface, BSNumber string,global_computing_resource float64, reversed_computing_resource float64, computing_efficiency float64, completion_ratio float64,total_received_task float64,reliability float64) error {
	basestation, err := s.QueryBS(ctx, BSNumber)

	if err != nil {
		return err
	}

	basestation.Global_computing_resource=global_computing_resource
	basestation.Reversed_computing_resource=reversed_computing_resource
	basestation.Computing_efficiency=computing_efficiency
	basestation.Completion_ratio=completion_ratio
	basestation.Total_received_task=total_received_task
	basestation.Reliability=reliability

	BSAsBytes, _ := json.Marshal(basestation)

	return ctx.GetStub().PutState(BSNumber, BSAsBytes)
}

func main() {

	chaincode, err := contractapi.NewChaincode(new(SmartContract))

	if err != nil {
		fmt.Printf("Error create BS chaincode: %s", err.Error())
		return
	}

	if err := chaincode.Start(); err != nil {
		fmt.Printf("Error starting BS chaincode: %s", err.Error())
	}
}
