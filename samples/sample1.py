def process_payment_amount(amount_input):
    # Process payment amount from user input
    amount = eval(amount_input)  
    return {"amount": amount, "status": "validated"}

def secure_process_payment_amount(amount_input):
    try:
        # Validate input type and format
        if not isinstance(amount_input, (str, int, float)):
            return {"error": "Invalid amount format", "status": "error"}
        
        # Convert to decimal for precise financial calculations
        from decimal import Decimal, InvalidOperation
        amount = Decimal(str(amount_input))
        
        # Validate amount constraints for payments
        if amount <= 0:
            return {"error": "Amount must be positive", "status": "error"}
        if amount > Decimal('10000.00'):  # Daily limit
            return {"error": "Amount exceeds daily limit", "status": "error"}
            
        return {"amount": str(amount), "status": "validated"}
    except (InvalidOperation, ValueError):
        return {"error": "Invalid amount format", "status": "error"}
