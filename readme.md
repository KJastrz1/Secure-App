# Secure Lending Platform

## Video presentation
[Link do wideo](assets/lendlist.mp4)

## Overview
This Secure Lending Platform is a simple web application designed with a focus on high security standards rather than functionality or performance. The primary aim is to provide a secure environment for users to lend and borrow money among themselves, ensuring robust authentication, secure data handling, and meticulous validation processes.

## Features

### Security-First Authentication
- **Strict Data Validation**: Adopts a pessimistic approach to input validation to prevent common security threats such as SQL injection, XSS, and other injection flaws.
- **Secure Password Storage**: Utilizes cryptographic hashing functions with added salt and pepper for secure password storage. Implements key stretching to enhance the security of stored passwords.

### Account Management
- **Email Verification**: After creating an account, the user must activate it by verifying their email address.
- **Password Recovery**: Allows users to recover access to their accounts in case of lost passwords through a secure process involving email verification.
- **Password Change Feature**: Users can change their passwords, which undergoes the same rigorous checks and storage methods as initial password creation.

### Loan Management
- **Recording New Loans**: Provides a secure form for lenders to record new loans, which then require confirmation by the borrower to ensure accuracy and consent.
- **Viewing Loan Records**: Borrowers can view their confirmed loans while lenders can track the status and repayment of lent amounts.

### Security Enhancements
- **Session Consistency Checks**: Implements anti-CSRF tokens to protect against Cross-Site Request Forgery.
- **Brute Force Protection**: Monitors failed login attempts and progressively delays password verification attempts to mitigate brute force attacks.
- **Password Strength Feedback**: Provides real-time feedback on password strength based on entropy and resistance to dictionary attacks.
- **Unusual New Login Notifications**: Alerts users to new logins from unknown devices or locations to detect potential unauthorized access.


## Technologies Used
- **Backend**: Python with Flask framework
- **Database**: SQLite
- **Frontend**: Minimalistic HTML5 and CSS with a focus on security over aesthetics

