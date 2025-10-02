def calculate_interest(principal, rate, time):
    return principal * rate * time

def calculate_interest_secure(principal, rate, time, user_id):
    import logging
    from decimal import Decimal, InvalidOperation
    
    logger = logging.getLogger('financial_calculations')
    
    try:
        # Convert to Decimal for precise financial calculations
        principal_decimal = Decimal(str(principal))
        rate_decimal = Decimal(str(rate))
        time_decimal = Decimal(str(time))
        
        # Validate business rules
        if principal_decimal <= 0:
            raise ValueError("Principal must be positive")
        if not (Decimal('0.01') <= rate_decimal <= Decimal('0.30')):
            raise ValueError("Interest rate must be between 1% and 30%")
        if time_decimal <= 0:
            raise ValueError("Time period must be positive")
        
        # Calculate interest
        interest = principal_decimal * rate_decimal * time_decimal
        
        # Log calculation for audit trail
        logger.info(f"Interest calculation for user {user_id}: "
                   f"P={principal_decimal}, R={rate_decimal}, T={time_decimal}, I={interest}")
        
        return str(interest)
        
    except (InvalidOperation, ValueError, TypeError) as e:
        logger.error(f"Invalid interest calculation for user {user_id}: {e}")
        raise ValueError(f"Invalid calculation parameters: {e}")
