clear;
clc;
data = csvread('feature_review_training-20000.csv',1,1);
test = csvread('feature_review_testing-20000.csv',1,1);

data = data(1:1000,:);%length(data),:);
test = test(1:1000,:);

% Labels
% review_id   true_stars   word_count  word_cap_count   text_polarity    biz_stars    biz_review_count   usr_avrstars   usr_review_count   usr_fans
%     0           1             2            3               4              5               6                 7               8               9      
    
%Adding 1 to polarity to keep it positive -  Range 0 - 2
data(:,4) = data(:,4)+1;
test(:,4) = test(:,4)+1;

% Taking ratings to compare
test_rating = test(:,1);

% Segregating Inputs for different distributions
lognormal_data  = [ data(:,1) data(:,2:3)];
lognormal_input = lognormal_data(:,2:end);
lognormal_test  = test(:,2:3);

beta_dist_data  = [ data(:,1) data(:,4)];
beta_dist_input = beta_dist_data(:,2:end);
beta_dist_test  =  test(:,4);

gamma_dist_data  = [ data(:,1) data(:,6) data(:,8)];
gamma_dist_input = gamma_dist_data(:,2:end);
gamma_dist_test  = [ test(:,6) test(:,8)];


stars = data(:,1);

classes = 5;
k = classes;

count_stars = zeros(1,k); % 9 as ratings considered are 1 1.5 2 2.5 3 3.5 4 4.5 5
prior = zeros(1,k);
class_assoc = zeros(size(data,1),1); % Maintains true class for calculating mean and variance

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Calculate prior probability

for i = 1:length(stars)    
      count_stars(stars(i)) = count_stars(stars(i)) + 1;
      class_assoc(i)        = stars(i);
end

total_stars = sum(count_stars);

for i = 1:length(count_stars)
    prior(i) = count_stars(i)/total_stars;
end

prior;

% Likelikhood for lognormal distributions
%logn_likelihood = lognormal_likelihood( lognormal_data, lognormal_input, lognormal_test, class_assoc, classes );

% Likelihood for Beta distributions
beta_likelihood = beta_likelihood( beta_dist_data, beta_dist_input, beta_dist_test, classes );

% Likelihood for Gamma distributions
%gamma_likelihood = gamma_likelihood( gamma_dist_data, gamma_dist_input, gamma_dist_test, classes );
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%posterior = zeros(1,9);

%final_likelihood = zeros(1,9);
%posterior = likelihood .* prior';
%final_likelihood = logn_likelihood .* beta_likelihood .* gamma_likelihood;
final_likelihood = beta_likelihood;

test_rating;

[maxA,ind] = max(final_likelihood');
predicted_rating = ind; %(ind/2)+0.5;

predicted_rating = predicted_rating';
incorrect_rating = (test_rating ~= predicted_rating);
output = [test_rating predicted_rating incorrect_rating];

sum(incorrect_rating);
length(incorrect_rating);
prediction_percentage = (length(incorrect_rating)-sum(incorrect_rating))*100/length(incorrect_rating);
%disp('Actual Stars  Predicted Stars ');
prediction_percentage




