// SPDX-License-Identifier: MIT

pragma solidity ^0.8.34;

contract Crowdfunding {
    // Créateur du projet
    address public creator;

    // Objectif financier
    uint public goal;

    // Date limite
    uint public deadline;

    // Montant total collecté
    uint public totalRaised;

    // Contributions de chaque utilisateur
    mapping(address => uint) public contributions;

    // Statut du projet
    bool public isFinalized;
    bool public goalReached;

    // Constructeur 
    constructor(uint _goal, uint _durationInDays) {
        creator = msg.sender; 
        // msg.sender = celui qui déploie le contrat
        goal = _goal;
        deadline = block.timestamp + (_durationInDays * 1 days);
        totalRaised = 0;
    }

    // Fonction pour contribuer
    function contribute() public payable {
        require(block.timestamp < deadline, "Deadline passed");
        // Vérifie que le projet est encore actif
        require(msg.value > 0, "Send some ETH");
        // Vérifie que l'utilisateur envoie de l'argent
        contributions[msg.sender] += msg.value;
        // Ajoute contribution utilisateur
        totalRaised += msg.value;
        // Ajoute au total
    }

    // Finaliser le projet
    function finalize() public {
        require(block.timestamp >= deadline, "Not ended yet");
        // Vérifie que la campagne est terminée
        require(!isFinalized, "Already finalized");
        // Empêche double exécution
        isFinalized = true;
        if (totalRaised >= goal) {
            goalReached = true;
        }
    }

    // Retirer les fonds (si succès)
    function withdraw() public {
        require(msg.sender == creator, "Not creator");
        require(goalReached, "Goal not reached");
        uint balance = address(this).balance;
        (bool success, ) = payable(creator).call{value: balance}("");
        require(success, "Withdraw failed");
    }

    // Remboursement 
    function refund() public {
        require(isFinalized, "Not finalized");
        require(!goalReached, "Goal was reached");
        uint amount = contributions[msg.sender];
        require(amount > 0, "No contribution");
        contributions[msg.sender] = 0;
        (bool success, ) = payable(msg.sender).call{value: amount}("");
        require(success, "Refund failed");
    }
}