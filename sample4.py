def process_payment_batch(payments):
    results = []
    for payment in payments:
        result = process_single_payment(payment)
        results.append(result)
    return results

def process_payment_batch_optimized(payments, max_concurrent=5):
    import asyncio
    from concurrent.futures import ThreadPoolExecutor
    import logging
    
    logger = logging.getLogger('payment_processing')
    
    # Limit concurrency for financial operations to avoid overwhelming downstream systems
    async def process_payment_with_semaphore(semaphore, payment):
        async with semaphore:
            try:
                # Add delay to respect rate limits for payment processor APIs
                await asyncio.sleep(0.1)
                
                # Process payment with proper error handling
                result = await process_single_payment_async(payment)
                
                # Log successful processing
                logger.info(f"Payment processed successfully: {payment['payment_id']}")
                return result
                
            except Exception as e:
                logger.error(f"Payment processing failed for {payment['payment_id']}: {e}")
                return {"payment_id": payment["payment_id"], "status": "failed", "error": str(e)}
    
    async def main():
        semaphore = asyncio.Semaphore(max_concurrent)
        tasks = [process_payment_with_semaphore(semaphore, payment) for payment in payments]
        return await asyncio.gather(*tasks, return_exceptions=True)
    
    return asyncio.run(main())
