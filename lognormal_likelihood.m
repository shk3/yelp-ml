function [ likelihood ] = lognormal_likelihood( lognormal_data, lognormal_input, lognormal_test, class_assoc, classes )

num_features_lognormal = size(lognormal_data,2)-1; % minus 1 since true_stars column not considered

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Calculating mu for the training set

mu = zeros(classes,num_features_lognormal);
class_count = zeros(classes,1);
N  = size(lognormal_data,1);

logx_val = zeros(1,num_features_lognormal);

for i=1:N
    
    class_count(class_assoc(i)) = class_count(class_assoc(i)) + 1;

    logx_val = log(lognormal_input(i,:));
    logx_val(isinf(logx_val)) = 0;

    mu(class_assoc(i),:) = mu(class_assoc(i),:) + logx_val;

    %temp_feature_wo_zero(temp_feature_wo_zero == 0) = [];
    %mu(1,j) = sum(log(temp_feature_wo_zero));  % j+1 as 1st row is true_stars    
     
end

for c=1:classes
    if class_count(c)~=0
        mu(c,:) = mu(c,:)/class_count(c);
    end
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Calculating variance for the training set

%Initialize covar:  d x d x k matrix - Identity Matrix
covar = eye(num_features_lognormal);
sum_covar = eye(num_features_lognormal);

logx_val = zeros(1,num_features_lognormal);

for c=1:classes
   covar(:,:,c) = eye(num_features_lognormal); 
   sum_covar(:,:,c) = eye(num_features_lognormal); 
end


for i=1:N
    logx_val = log(lognormal_input(i,:));
    logx_val(isinf(logx_val)) = 0;
    sum_covar(:,:,class_assoc(i)) = sum_covar(:,:,class_assoc(i)) + ...
        ((logx_val-mu(class_assoc(i),:))'*(logx_val-mu(class_assoc(i),:)));
end 

for c=1:classes
    if(det(sum_covar(:,:,c))<0.0001)
        sum_covar(:,:,c) = sum_covar(:,:,c) + 0.001 .* eye(num_features_lognormal);
    end
    
    if class_count(c)~=0
        covar(:,:,c) = sum_covar(:,:,c)/class_count(c);
    end
end

%Calcualte likelihood from the distribution function for lognormal
length(lognormal_test);
  likelihood = zeros(length(lognormal_test),classes);
  for entry=1:length(lognormal_test)
    for c=1:classes

        log_ip_lower = log(lognormal_test(entry,:));
        log_ip_lower(isinf(log_ip_lower))=0;


        log_ip_higher = log(lognormal_test(entry,:)+1);
        log_ip_higher(isinf(log_ip_higher))=0;


       % likelihood_calc(c,1) = exp((-0.5) * ( (log_ip-mu(c,:)) * (log_ip-mu(c,:))' ) ./ sigma(:,:,c));
       % likelihood(c,1) = (0.3989*likelihood_calc(c,1)) ./ (lognormal_test.*sqrt(sigma(:,:,c)));   % 1/root(2*pi) = 0.3989 

       likelihood(entry,c) = mvncdf(log_ip_higher,mu(c,:),covar(:,:,c)) - mvncdf(log_ip_lower,mu(c,:),covar(:,:,c));
       
    end
  end
  likelihood;
end

