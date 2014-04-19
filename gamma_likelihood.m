function [ gamma_likelihood ] = gamma_likelihood( gamma_dist_data, gamma_dist_input, gamma_dist_test, classes )
%GAMMA_DIST_LIKELIHOOD Summary of this function goes here
%   Detailed explanation goes here

num_features_gamma = size(gamma_dist_data,2)-1; % minus 1 since true_stars column not considered


% Training
gamma_params = zeros(classes,1); % Here 1 states the paramters from output of gamma function(Internally 2)


%a((a(:,1)==i),:)
  
% Calculating parameters for every class and features
for j=1:num_features_gamma
    output = [];
    for k=1:classes
        gamma_params = gamfit( gamma_dist_input((gamma_dist_data(:,1)==k),j) );
        output = vertcat (output,gamma_params);
    end
    
    param_matrix(:,:,j) = output;
    
end


% Testing
gamma_likelihood = ones(length(gamma_dist_test),classes);

for j=1:num_features_gamma
    p = param_matrix(:,:,j);
    for i=1:length(gamma_dist_test)
        for c=1:classes
            gamma_likelihood(i,c) = gamma_likelihood(i,c) * gampdf(gamma_dist_test(i,j),p(c,1),p(c,2)); %Multiplying each likelihood for class for all features as naive bayes
        end
    end
end


end