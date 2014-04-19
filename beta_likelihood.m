function [ beta_likelihood ] = beta_likelihood( beta_dist_data, beta_dist_input, beta_dist_test, classes )
%beta_DIST_LIKELIHOOD Summary of this function goes here
%   Detailed explanation goes here

num_features_beta = size(beta_dist_data,2)-1; % minus 1 since true_stars column not considered


% Training
beta_params = zeros(classes,1); % Here 1 states the paramters from output of beta function(Internally 2)

%a((a(:,1)==i),:)
  
% Modifying the input since Beta function requires [0 1]
% Normalizing
max_f = [2];%[2 5];
min_f = [0];%[0 1];
for j=1:num_features_beta
    max_ip = max_f(j);%max(beta_dist_input(:,j));
    min_ip = min_f(j);%min(beta_dist_input(:,j));
    
    max_test = max_f(j);%max(beta_dist_test(:,j));
    min_test = min_f(j);%min(beta_dist_test(:,j));
    
    for i=1:length(beta_dist_input)
       beta_dist_input(i,j) = (beta_dist_input(i,j)-min_ip)/(max_ip-min_ip);
       beta_dist_test(i,j)  = (beta_dist_test(i,j)-min_test)/(max_test-min_test);
    end
end
param_matrix = [];
% Calculating parameters for every class and features
for j=1:num_features_beta
    output = [];
    for k=1:classes
        beta_params = betafit( beta_dist_input((beta_dist_data(:,1)==k),j) );
        output = vertcat (output,beta_params);
    end
    
    param_matrix(:,:,j) = output;
    
end

% a = beta_dist_input((beta_dist_data(:,1)==5),:);
% hist(a);

% b = param_matrix(:,:,1);
% b
% figure();
% plot(betapdf(0:0.01:1,b(5,1),b(5,2)));

% Testing
beta_likelihood = ones(length(beta_dist_test),classes);

for j=1:num_features_beta
    p = param_matrix(:,:,j);
    for i=1:length(beta_dist_test)
        for c=1:classes
            beta_likelihood(i,c) = beta_likelihood(i,c) * betapdf(beta_dist_test(i,j),p(c,1),p(c,2)); %Multiplying each likelihood for class for all features as naive bayes
        end
    end
end


end