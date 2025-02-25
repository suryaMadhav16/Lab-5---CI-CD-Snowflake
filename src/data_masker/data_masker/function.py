import re

def mask_email(email, level='medium'):
    """Mask an email address based on the specified level"""
    if not email or '@' not in email:
        return email
        
    username, domain = email.split('@')
    domain_parts = domain.split('.')
    
    if level == 'high':
        # High masking: completely hide username and domain
        masked_username = '*' * len(username)
        masked_domain = '*' * len(domain_parts[0]) + '.' + domain_parts[1]
    elif level == 'medium':
        # Medium masking: show first character of username and domain
        masked_username = username[0] + '*' * (len(username) - 1)
        masked_domain = domain_parts[0][0] + '*' * (len(domain_parts[0]) - 1) + '.' + domain_parts[1]
    else:  # low
        # Low masking: show first and last character
        if len(username) > 2:
            masked_username = username[0] + '*' * (len(username) - 2) + username[-1]
        else:
            masked_username = username[0] + '*' * (len(username) - 1)
        masked_domain = domain
        
    return f"{masked_username}@{masked_domain}"

def mask_phone(phone, level='medium'):
    """Mask a phone number based on the specified level"""
    if not phone:
        return phone
        
    # Remove non-digit characters for processing
    digits = re.sub(r'\D', '', phone)
    
    if level == 'high':
        # High masking: show only last 2 digits
        masked = 'X' * (len(digits) - 2) + digits[-2:]
    elif level == 'medium':
        # Medium masking: show only last 4 digits
        masked = 'X' * (len(digits) - 4) + digits[-4:]
    else:  # low
        # Low masking: show last 7 digits (hide area code)
        masked = 'X' * (len(digits) - 7) + digits[-7:]
    
    # Reapply formatting if original had formatting
    if '-' in phone:
        if len(digits) == 10:  # US format
            return f"{'X' * 3}-{'X' * 3}-{digits[-4:]}"
        else:
            # Best effort to maintain original format
            return re.sub(r'\d', 'X', phone[:-4]) + phone[-4:]
    
    return masked

def mask_credit_card(cc_number, level='medium'):
    """Mask a credit card number based on the specified level"""
    if not cc_number:
        return cc_number
        
    # Remove non-digit characters for processing
    digits = re.sub(r'\D', '', cc_number)
    
    if level == 'high':
        # High masking: show only last 4 digits
        masked = 'X' * (len(digits) - 4) + digits[-4:]
    elif level == 'medium':
        # Medium masking: show first digit and last 4 digits
        masked = digits[0] + 'X' * (len(digits) - 5) + digits[-4:]
    else:  # low
        # Low masking: show first and last 4 digits, mask middle
        masked = digits[:4] + 'X' * (len(digits) - 8) + digits[-4:]
    
    # Reapply formatting if original had formatting
    if '-' in cc_number:
        formatted = ''
        i = 0
        for char in cc_number:
            if char == '-':
                formatted += '-'
            else:
                if i < len(masked):
                    formatted += masked[i]
                    i += 1
                else:
                    formatted += 'X'
        return formatted
    
    return masked

def mask_ssn(ssn, level='medium'):
    """Mask a Social Security Number based on the specified level"""
    if not ssn:
        return ssn
        
    # Remove non-digit characters for processing
    digits = re.sub(r'\D', '', ssn)
    
    if level == 'high':
        # High masking: mask all digits
        masked = 'X' * len(digits)
    elif level == 'medium':
        # Medium masking: show only last 4 digits
        masked = 'X' * (len(digits) - 4) + digits[-4:]
    else:  # low
        # Low masking: show only last 4 digits
        masked = 'X' * (len(digits) - 4) + digits[-4:]
    
    # Reapply formatting if original had formatting
    if '-' in ssn and len(digits) == 9:
        return f"XXX-XX-{digits[-4:]}"
    
    return masked

def main(value, type='email', level='medium'):
    """
    Main entry point for the UDF
    
    Args:
        value (str): The value to mask
        type (str): Type of data - 'email', 'phone', 'credit_card', or 'ssn'
        level (str): Masking level - 'high', 'medium', or 'low'
    
    Returns:
        str: The masked value
    """
    if not value:
        return value
        
    if type.lower() == 'email':
        return mask_email(value, level)
    elif type.lower() == 'phone':
        return mask_phone(value, level)
    elif type.lower() == 'credit_card':
        return mask_credit_card(value, level)
    elif type.lower() == 'ssn':
        return mask_ssn(value, level)
    else:
        # Default behavior - return as is if type not recognized
        return value
