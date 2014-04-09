data = csvread('feature_review.csv',1,1);
test = data(5,2:end);
test
input = data(:,2:end);

stars = data(:,1);

classes = 9;
k = classes;

num_features = size(data,2)-1; % minus 1 since true_stars column not considered

count_stars = zeros(1,9); % 9 as ratings considered are 1 1.5 2 2.5 3 3.5 4 4.5 5
prior = zeros(1,9);
class_assoc = zeros(size(data,1),1); % Maintains true class for calculating mean and variance

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Calculate prior probability

for i = 1:length(stars)
    
    if ( mod(stars(i),1)>0)
        count_stars(2*(stars(i)-0.5)) = (count_stars(2*(stars(i)-0.5))) + 1;
        class_assoc(i) = 2*(stars(i)-0.5);
    else 
        count_stars(2*stars(i)-1) = count_stars(2*stars(i)-1) + 1;
        class_assoc(i) = 2*stars(i)-1;
    end
end

total_stars = sum(count_stars);

for i = 1:length(count_stars)
    prior(i) = count_stars(i)/total_stars;
end

prior;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Calculating mu for the training set

mu = zeros(k,num_features);
class_count = zeros(classes,1);
N  = size(data,1);

logx_val = zeros(1,num_features);

for i=1:N
    
    class_count(class_assoc(i)) = class_count(class_assoc(i)) + 1;

    logx_val = log(input(i,:));
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
covar = eye(num_features);
sum_covar = eye(num_features);

logx_val = zeros(1,num_features);

for c=1:classes
   covar(:,:,c) = eye(num_features); 
   sum_covar(:,:,c) = eye(num_features); 
end



%sum_covar(:,:,c)=zeros(num_features,num_features);

for i=1:N
    logx_val = log(input(i,:));
    logx_val(isinf(logx_val)) = 0;
    sum_covar(:,:,class_assoc(i)) = sum_covar(:,:,class_assoc(i)) + ...
        ((logx_val-mu(class_assoc(i),:))'*(logx_val-mu(class_assoc(i),:)));
end 

for c=1:classes
    if(det(sum_covar(:,:,c))<0.0001)
        sum_covar(:,:,c) = sum_covar(:,:,c) + 0.001 .* eye(num_features);
    end
    
    if class_count(c)~=0
        covar(:,:,c) = sum_covar(:,:,c)/class_count(c);
    end
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Calcualte likelihood from the distribution function for lognormal
likelihood_calc = zeros(classes,1);
likelihood = zeros(classes,1);

for c=1:classes
    
    log_ip_lower = log(test);
    log_ip_lower(isinf(log_ip_lower))=0;
    
    
    log_ip_higher = log(test+1);
    log_ip_higher(isinf(log_ip_higher))=0;
    
    
   % likelihood_calc(c,1) = exp((-0.5) * ( (log_ip-mu(c,:)) * (log_ip-mu(c,:))' ) ./ sigma(:,:,c));
   % likelihood(c,1) = (0.3989*likelihood_calc(c,1)) ./ (test.*sqrt(sigma(:,:,c)));   % 1/root(2*pi) = 0.3989 

   likelihood(c,1) = mvncdf(log_ip_higher,mu(c,:),covar(:,:,c))  - mvncdf(log_ip_lower,mu(c,:),covar(:,:,c));
   
   
   
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
posterior = zeros(1,9);

posterior = likelihood .* prior';






