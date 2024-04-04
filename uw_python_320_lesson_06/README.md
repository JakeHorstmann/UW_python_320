# Introduction

At this point, you have successfully managed to implement your Social Network project using both relational and non-relational databases. Both implementations have their merits and their shortcomings. Beyond subjective appreciation of these, we would like you to collect some data to compare both in terms of overall performance, bottlenecks and potential for improvements.

# What you need to do

Your starting point will be the code from your SQL Database implementation from lesson 3 and your MongoDB implementation from lesson 5.

Make sure both implementations start from empty databases, so that it can be a fair comparison.

As part of the assignment, we are providing you with a new set of account and status update data, all in CSV format. To make things more interesting, we have doubled the number of user accounts to 2,000 and the number of status updates to 200,000. This will help emphasize any differences in performance.

Same as before, if you want to try generating your own source data and increase the amount of data your code will need to process, you can use the following Github repository as a reference: https://github.com/ldconejo/social_network_generator

1. Use some of the profiling tools you have learned in lesson 6 and collect performance data from your SQL and MongoDB implementations on the following tasks:
    * Load user database from a CSV file.
    * Load status database from a CSV file.
    * Add a user / status update.
    * Update a user / status update.
    * Search for a user / status update.
    * Delete a user / status update.

1. Prepare a summary of your results, including side-by-side comparisons of each of the database implementations doing the tasks outlined above. As a suggestion, you can use the same .md (metadata) format used by this file to provide your report. RST format is also acceptable.

1. Based on your results and on **your experience implementing both databases**, make a recommendation as to which one should be implemented. Performance is key, but include other technical aspects such as ease of implementation if appropriate.

# What you need to submit

* Include the code from both database implementations, in separate folders. **Do not** include any CSV files.

* Include any raw files with your performance results.

* Include your report on those results and your recommendation.

# Tips

This is a comparatively easy assignment, if you find yourself with some extra time, try to start working on assignment 7, which requires you to implement parallelization within your MongoDB project.
 